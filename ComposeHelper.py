import base64
import os.path
import random
import string
import subprocess
import sys
import time

import docker
import yaml

from model.validconfig import ValidConfig


class ComposeHelper:
    config = None
    compose = None
    waiter_dependencies = []
    _healthcheck_template = {
        'interval': '10s',
        'timeout': '10s',
        'retries': 5,
        'start_period': '30s'
    }

    def __init__(self, config: ValidConfig):
        self.process = None
        self.config = config.dict()
        self.build_template()
        self.workdir = os.path.abspath('images/')

    def get_random_string(self, length) -> str:
        # choose from all lowercase letter
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(length))

    def build_template(self):
        bridge_name = "br-" + self.get_random_string(10)
        test_name = self.config['settings']['name']
        self.compose = {
            'version': "3.8",
            'volumes': {'config': None},
            'networks': {'default': {'driver_opts': {'com.docker.network.bridge.name': bridge_name}}},
            'services': {
                'base': {'build': './utils/base', 'deploy': {'mode': 'replicated', 'replicas': 0},
                         'image': 'covert-base'},
                'sniffer': {'build': './utils/sniffer',
                            'cap_add': ['NET_ADMIN', 'NET_RAW'],
                            'network_mode': 'host',
                            'environment': ['INTERFACE_NAME=' + bridge_name, 'SIM_NAME=' + test_name],
                            'volumes': ['./output/pcaps:/pcaps'],
                            'healthcheck': self._healthcheck_template.copy()
                            }
            }
        }
        self.compose['services']['sniffer']['healthcheck']['test'] = ['CMD', 'pgrep', 'tcpdump']

    def build_server(self, protocol_object):
        """ this is where we generate the """
        hostname = protocol_object['server']['host']
        port = protocol_object['server']['port']
        image = protocol_object['server']['image']
        path = protocol_object['server']['path']
        if not protocol_object['server']['internal']:
            print("{}:{} is marked as external server in config, please make sure that it is up and reachable".format(
                hostname, port), file=sys.stderr)
            return
        healthcheck = ["CMD"]
        healthcheck += protocol_object['server']['healthcheck'].split()
        tmp = {'depends_on': {'sniffer': {'condition': 'service_healthy'}},
               'ports': ["{}:{}".format(port, port)],
               'environment': ['TARGET_PORT=' + str(port)],
               'healthcheck': self._healthcheck_template.copy()
               }
        tmp['healthcheck']['test'] = healthcheck
        if image:
            tmp['image'] = str(image)
        elif path:
            path = self.workdir + '/' + path
            path = os.path.relpath(path, self.workdir)
            tmp['build'] = './' + str(path)
        else:
            print("{} is not external and neither an image nor a path is provided".format(hostname), file=sys.stderr)
            raise RuntimeError("config error")
        self.compose['services'][hostname] = tmp.copy()
        self.waiter_dependencies.append(hostname)
        pass

    def build_waiter(self):
        """if we have internal servers, we need to add a waiter that makes sure that the servers are running"""
        tmp = {'build': './utils/waiter', 'depends_on': {}}
        depends_template = {'condition': 'service_healthy'}
        for elem in self.waiter_dependencies:
            tmp['depends_on'][elem] = depends_template
        self.compose['services']['waiter'] = tmp.copy()

    def build_client(self, protocol_object):
        name = protocol_object['client']['host']
        image = protocol_object['client']['image']
        path = protocol_object['client']['path']
        server = protocol_object['server']['host']
        port = protocol_object['server']['port']
        replicas = protocol_object['client']['instances']
        tmp = {'deploy': {'replicas': replicas},
               'volumes': ["config:/config"],
               'depends_on': ['waiter'],
               'environment': ['TARGET_HOST=' + server, 'TARGET_PORT=' + str(port), 'SEND_INTERVAL=' + str(protocol_object['time_interval'])]
               }
        if image:
            tmp['image'] = str(image)
        elif path:
            path = self.workdir + '/' + path
            path = os.path.relpath(path, self.workdir)
            tmp['build'] = './' + str(path)
        else:
            print("{} has no image or path provided".format(name), file=sys.stderr)
            raise RuntimeError("config error")
        self.compose['services'][name] = tmp.copy()

    def build_covert(self, protocol_object, channel):
        name = channel + "-" + self.get_random_string(10)
        path = protocol_object['channels'][channel]['path']
        image = protocol_object['channels'][channel]['image']
        server = protocol_object['server']['host']
        port = protocol_object['server']['port']
        exploited_clients = protocol_object['channels'][channel]['exploited_clients']
        covert_file = protocol_object['channels'][channel]['covert_file']
        covert_string = protocol_object['channels'][channel]['covert_str']
        tmp = {'depends_on': ['waiter'],
               'volumes': ["config:/config"],
               'environment': ['TARGET_HOST=' + server, 'TARGET_PORT=' + str(port), 'SEND_INTERVAL=' + str(protocol_object['time_interval'])]
               }
        if image:
            tmp['image'] = str(image)
        elif path:
            path = self.workdir + '/' + path
            path = os.path.relpath(path, self.workdir)
            tmp['build'] = './' + str(path)
        else:
            print("Covert channel {} has no image or path.".format(channel), file=sys.stderr)
            raise RuntimeError("config error")
        if protocol_object['client']['instances'] < exploited_clients:
            print("not enough clients for simulation of {}".format(channel), file=sys.stderr)
            raise RuntimeError("config error")
        protocol_object['client']['instances'] -= exploited_clients
        covert_message = None
        if covert_string:
            covert_message = base64.b64encode(covert_string.encode('utf-8'))
        elif covert_file:
            try:
                with open(covert_file, 'rb') as f:
                    content = f.read()
                    covert_message = base64.b64encode(content)
            except FileNotFoundError as e:
                print("ERROR - {} not found - using random values instead".format(covert_file), file=sys.stderr)
        if not covert_message:
            covert_message = base64.b64encode(self.get_random_string(10240).encode('utf-8'))
        tmp['environment'].append("COVERT_MESSAGE=" + covert_message.decode('utf-8'))
        tmp['environment'].append("COVERT_VICTIMS=" + str(exploited_clients))
        self.compose['services'][name] = tmp.copy()

    def read(self):
        """ helper for reading a manually created docker-compose file - todo remove this once it's no longer needed"""
        with open("docker-compose.yml", 'r') as f:
            self.compose = yaml.safe_load(f)

    def write(self):
        """write the config to a docker-compose file"""
        with open(self.workdir + '/docker-compose.yml', 'w') as f:
            yaml.dump(self.compose, f, default_flow_style=False)

    def run(self) -> bool:
        """ start the simulation"""
        print("removing old docker networks: ", end='')
        self.process = subprocess.run(["docker", "network", "prune", "-f"], capture_output=False)
        output_path = self.workdir + "/output"
        try:
            os.mkdir(output_path)
            output_path = output_path + "/pcaps"
            os.mkdir(output_path)
        except FileExistsError:
            pass
        except FileNotFoundError:
            print("unable to create {} directory - parent directory does not exist".format(output_path))
        if self.process.returncode:
            print("failed - please run docker network prune manually before starting the simulation")
            return False
        print("done")
        print("starting the simulation... ", end='')
        self.process = subprocess.run(["docker-compose", "up", "--build", "--force-recreate", "-d"],
                                      capture_output=True, cwd=self.workdir)
        if self.process.returncode:
            print("failed - Output: ")
            print(self.process.stderr, file=sys.stderr)
            print(self.process.stdout, file=sys.stdout)
            return False
        print("done")
        return True

    def stop(self) -> bool:
        print("capturing the simulation log... ", end='')
        try:
            self.process = subprocess.run(["docker-compose", "logs", "-t"], capture_output=True, cwd=self.workdir)
            log_name = "{}/output/{}_{}.log".format(self.workdir, self.config['settings']['name'], int(time.time()))
            with open(log_name, 'wb') as f:
                f.write(self.process.stdout)
            print("done")
        except Exception as e:
            print("failed - error: {}".format(e))
        print("stopping the simulation... ", end='')
        self.process = subprocess.run(["docker-compose", "down", "-t 30", "-v", "--remove-orphans"], capture_output=True, cwd=self.workdir)
        if self.process.returncode:
            print("maybe failed (docker-compose down sometimes returns 1 despite shutting down cleanly) - Output: ")
            print(self.process.stderr, file=sys.stderr)
            print(self.process.stdout, file=sys.stdout)
            return False
        print("done")
        return True

    def generate(self):
        """this is where we generate the docker-compose file out of our own config file"""
        for protocol in self.config['protocols']:
            protocol_obj = self.config['protocols'][protocol]
            if protocol_obj['server']['internal']:
                self.build_server(protocol_obj)
            if protocol_obj['client']['instances'] > 0:
                self.build_client(protocol_obj)
            for channel in protocol_obj['channels']:
                self.build_covert(protocol_obj, channel)
        if self.waiter_dependencies:
            self.build_waiter()
        service_lower = {}
        for key, value in self.compose['services'].items():
            service_lower[key.lower()] = value
        self.compose['services'] = service_lower

    def wait(self) -> bool:
        """
        this is where we wait for the simulation to finish
        """
        print("waiting for the simulation to finish or time out.. ", end='')
        maximum_time = self.config['settings']['time_quit']
        if maximum_time:
            # Sleep for the specified time, then shutdown the simulation
            time.sleep(maximum_time)
            print("timeout")
            return True
        # else check if all covert-channels terminated
        cli = docker.DockerClient()
        not_finished = True
        while not_finished:
            time.sleep(10)
            containers = cli.containers.list(sparse=False)
            not_finished = False
            for container in containers:
                if not container.labels:
                    continue
                if 'com.docker.compose.project.working_dir' not in container.labels:
                    continue
                if self.workdir != container.labels['com.docker.compose.project.working_dir']:
                    continue
                if 'com.docker.compose.service' not in container.labels:
                    continue
                if 'Covert' in container.labels:
                    not_finished = True
                    break
        print("done")
        return True

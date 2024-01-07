import os
import random
import yaml
from filelock import Timeout, FileLock


config_file = '/config/mqtt.yml'

def mqtt_register_client(type: str, client_id: str, topic: str):
    """
    this function is a helper that registers a mqtt_client
    we need this function to let the covert channel know about existing mqtt clients
    locking is implemented as .lock file since other methods don't work inside docker 
    """
    os.makedirs(os.path.dirname(config_file), exist_ok=True)
    lock = FileLock(config_file + ".lock")
    with lock:
        data = {}
        if os.path.exists(config_file):
            with open(config_file, "r") as f:
                data = yaml.safe_load(f)
        # modify config
        if not 'mqtt' in data:
            data['mqtt'] = {}
        if not 'subscriber' in data['mqtt']:
            data['mqtt']['subscriber'] = {}
        data['mqtt']['subscriber'][client_id] = {'used-by': None, 'topic': topic, 'type': type}
        with open(config_file, 'w+') as f:
            yaml.dump(data, f)

def mqtt_register_covert(pattern: str, victim_type: str, covert_id: str, num_clients: int) -> list:
    """
    this function is a helper that adopts the mqtt_covert_channel
    we need this function to let the covert channel know about existing mqtt clients
    locking is implemented as .lock file since other methods don't work inside docker
    :return list of client_ids to use for covert channel 
    """
    victim_list = []
    os.makedirs(os.path.dirname(config_file), exist_ok=True)
    lock = FileLock(config_file + ".lock")
    with lock:
        data = {}
        if os.path.exists(config_file):
            with open(config_file, "r") as f:
                data = yaml.safe_load(f)
        # modify config
        if not victim_type in data['mqtt']:
            print("no possible victims of {} do exist".format(victim_type))
            return victim_list
        # find possible victims that are not yet used by other covert channels
        for victim in data['mqtt'][victim_type]:
            if not data['mqtt'][victim_type][victim]['used-by']:
                victim_list.append(victim)
        if len(victim_list) < num_clients:
            print("unable to startup {} - not enough possible victims".format(covert_id))
            return victim_list
        # lets randomly select num_clients to use for the covert channel
        random.shuffle(victim_list)
        del victim_list[num_clients:]
        for victim in victim_list:
            data['mqtt'][victim_type][victim]['used-by'] = covert_id
        if not 'covert' in data['mqtt']:
            data['mqtt']['covert'] = {}
        # insert the covert channel - should not be necessary but just for documentation
        data['mqtt']['covert'][covert_id] = {'used-clients': num_clients, 'pattern': pattern}
        # dump the config
        with open(config_file, 'w+') as f:
            yaml.dump(data, f)
    return victim_list


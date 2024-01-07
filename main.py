import grp
import os
import sys
import argparse

import yaml
from pydantic import ValidationError

from ComposeHelper import ComposeHelper
from model.validconfig import ValidConfig


def check_permissions() -> bool:
    uid = os.getuid()
    if uid == 0:
        return True
    username = os.getlogin()
    try:
        groups = grp.getgrnam("docker")
        if username in groups.gr_mem:
            return True
        print("insufficient privileges - make sure {} is in docker group".format(username))
    except KeyError:
        print("insufficient software - please install docker", file=sys.stderr)
    return False


def read_config(filename: str):
    config = None
    with open(filename, 'r') as file:
        config = yaml.safe_load(file)
    return config


def validate_config(config):
    valid = None
    try:
        valid = ValidConfig(**config)
    except ValidationError as e:
        print("Config is invalid", file=sys.stderr)
        print(e, file=sys.stderr)
    return valid


def generate_docker(config: ValidConfig):
    return


if __name__ == "__main__":
    # parse arguments
    parser = argparse.ArgumentParser(
        prog='covert-gen',
        description='this program creates and runs a simulation environment for covert channels',
        epilog='created 2023 by Katharina Lipsky')
    parser.add_argument("--filename", default='config.yml', required=False, help='path to the config file - default: config.yml')
    args = parser.parse_args()
    if not check_permissions():
        sys.exit(1)
    config = read_config(filename=args.filename)
    config = validate_config(config)
    if not config:
        print("Config is invalid - exiting", file=sys.stderr)
        sys.exit(1)

    hlp = ComposeHelper(config=config)
    hlp.generate()
    hlp.write()
    hlp.read()
    if not hlp.run():
        sys.exit(1)
    if not hlp.wait():
        sys.exit(1)
    if not hlp.stop():
        sys.exit(1)
    print("all done")

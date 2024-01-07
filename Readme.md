# Covert Channel simulation framework

## Dependencies
This generator needs
* a Linux operating system
* `python3` with `pip`
* `docker`
* the running user to be member of the `docker` group

in order to work properly.

## Installation
This guide is a best practice for ubuntu. Installation on other linux distributions may vary
### Installation of dependencies
#### Docker
The easiest way to install docker is to follow [dockers official installation guide](https://docs.docker.com/engine/install/ubuntu/).

After installing docker, ensure that all users running the generator are in the docker group and install the additional software docker-compose:
```bash
user@host:~/master/generator$ sudo usermod -aG docker $USER
user@host:~/master/generator$ sudo apt install -y docker-compose
```

#### Python
In order to execute the generator, python3 and pip must be installed.

There are several ways to do this. The easiest way is to just install the components if missing.
```bash
user@host:~/master/generator$ sudo apt update && \
sudo apt install -y python3 python3-pip
```

#### Pip Modules
in order to install the required python modules for the generator, 
you need to install the required python modules via `pip`.
```bash
user@host:~/master/generator$ pip install --upgrade pip
user@host:~/master/generator$ pip install -r requirements.txt
```
This step has to be repeated for every user account that executes the generator.

## Generating a config
Several sample configs are provided. 
It should be relatively easy to build your own config.
The generator checks for syntax errors in the config.
If the validation does not pass, an error will be printed.

## Executing
after building a valid config, the simulation can be started by running the `main.py` script.

The help function is a good starting point.
```bash
user@host:~/master/generator$ python3 main.py -h
```

## Other
### Generating your own images
The main priority of the generator is easy extensibility.
The existing images can be easily extended by adding containers into the image folder.
The only current exception is adding a protocol.
In order to add a protocol, it must also be included in the list `model/validconfig.py:ProtocolEnum{}` 

The generator will provide the following data to the containers
* shared volumes
```
/config/ # a shared folder between all clients and covert channels
```
* environment variables
```
# clients and covert channels
TARGET_HOST #the server hostname to connect to
TARGET_PORT #the port of the server (can be udp or tcp)
SEND_INTERVAL #the interval that is expected between single requests
# only for covert channels
COVERT_VICTIMS # how many other clients should be used for the covert channel
COVERT_MESSAGE # the byte message that should be transmitted encoded in base64
```
## Limitations
- currently only small covert messages can be transmitted (<1MB)
- currently only one simulation can be started in parallel.
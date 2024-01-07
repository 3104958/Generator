import random
import os
import uuid
import json
from paho.mqtt import client as mqtt_client
from utilities_mqtt import mqtt_register_client

config = { 'broker': os.environ.get('TARGET_HOST', '127.0.0.1'),
            'port': int(os.environ.get('TARGET_PORT', '1883')),
            'client_id': str(uuid.uuid4()),
            'topic': "python/mqtt",
            'used_by': None
}


def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(config['client_id'])
    # client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(config['broker'], config['port'])
    return client


def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")

    client.subscribe(config['topic'])
    client.on_message = on_message


def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()


if __name__ == '__main__':
    print("Starting - Client-ID: {}".format(config['client_id']))
    mqtt_register_client(type="subscriber", client_id=config['client_id'], topic=config['topic'])
    print("Config file written")
    run()

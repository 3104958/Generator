import base64
import os
import random
import sys
import time
import socket
from utilities import convert_pattern
from scapy.contrib import coap

config = {'server': os.environ.get('TARGET_HOST', '127.0.0.1'),
          'port': int(os.environ.get('TARGET_PORT', '5683')),
          'pattern': "coap-pt16-reset",
          'covert_message': os.environ.get('COVERT_MESSAGE', b""),
          'covert_victims': int(os.environ.get('COVERT_VICTIMS', "0")),
          'covert_delay': float(os.environ.get('SEND_INTERVAL', "3.0")),
          'used_by': None
          }


def run(value):
    message_id = random.randint(0, 65535)  # 0x0000 to 0xFFFF

    count = 0
    while count <= value:
        # we need a bound udp socket to prevent icmp unreachable answers to be generated
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((config['server'], config['port']))
            handshake = sock.recv(1024)
            # change to true if you want to actually send a coap request
            if False:
                # send handshake back to start the connection
                sock.sendall(handshake)
                packet = bytes(coap.CoAP(type=0, code=1, options=[('Uri-Path', b'time')]))
                # change byte 0 to 0x50 to represent tcp request
                packet = b'\x50' + packet[1:]
                # remove the message_id from packet since it's tcp (bytes 2 and 3)
                packet = packet[:2] + packet[4:]
                sock.sendall(packet)
        count += 1


if __name__ == '__main__':
    # parsing TARGET_HOST to the ip
    config['server'] = socket.gethostbyname(config['server'])
    time.sleep(10)
    print("Starting CoAP retransmission Covert Channel, config: {}".format(config))
    message = base64.b64decode(config['covert_message'])
    if config['covert_victims'] != 0:
        print("this channel doesn't exploit other clients - please adopt your config")
        exit(1)

    pattern = convert_pattern(message, 2)
    print("len(pattern) == {}".format(len(pattern)))
    while (pattern):
        current = pattern[0]
        run(current)
        pattern = pattern[1:]
        if (pattern):
            time.sleep(config['covert_delay'])
    sys.exit(0)

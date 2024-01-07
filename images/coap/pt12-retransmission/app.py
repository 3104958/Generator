import base64
import os
import random
import sys
import time
import socket
from utilities import convert_pattern
from scapy.all import IP, UDP, send
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
        source_port = random.randint(1024, 65535)
        # we need a bound udp socket to prevent icmp unreachable answers to be generated
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(('0.0.0.0', source_port))
        packet = IP(dst=config['server']) / UDP(sport=source_port, dport=config['port']) / coap.CoAP(type=0, msg_id=message_id,
                                                                                           code=1,
                                                                                           options=[
                                                                                               ('Uri-Path', b'time')])
        send(packet, verbose=False)
        count += 1
        sock.close()


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

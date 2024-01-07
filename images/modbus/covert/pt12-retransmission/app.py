import os
import base64
import socket

from RetransmitClient import RetransmitClient

from utilities import convert_pattern, print_host

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    TARGET_HOST = os.environ.get('TARGET_HOST', '172.19.0.2')
    TARGET_PORT = int(os.environ.get('TARGET_PORT', 502))
    COVERT_MESSAGE = os.environ.get('COVERT_MESSAGE', "ZXJyb3Itbm8tbXNn")
    print_host()
    try:
        COVERT_MESSAGE = base64.b64decode(COVERT_MESSAGE)
    except:
        print("ERROR: Unable to parse base64 covert message: {}".format(COVERT_MESSAGE))
        exit(1)
    print("Peer: {}:{}".format(TARGET_HOST, TARGET_PORT))
    print("Covert message: {}".format(COVERT_MESSAGE))
    print("blocking RST packets via iptables rule (see TcpSession.py)")
    os.system("iptables -A OUTPUT -p tcp --sport 1024:65535 --dport 502 --tcp-flags RST RST -j DROP")
    client = RetransmitClient()
    client.set_endpoint(TARGET_HOST, TARGET_PORT)
    client.set_covert_data(COVERT_MESSAGE)
    client.run()
    print("done")
    exit(0)

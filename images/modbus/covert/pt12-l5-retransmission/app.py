import random
import sys
import time
import socket
import os
import base64

from utilities import convert_pattern, print_host

if __name__ == '__main__':
    HOST = os.environ.get('TARGET_HOST', "127.0.0.1")  # The server's hostname or IP address
    PORT = os.environ.get('TARGET_PORT', 502)  # The port used by the server
    SEND_INTERVAL = os.environ.get('SEND_INTERVAL', 0.5) # how many seconds between messages
    PORT = int(PORT)
    SEND_INTERVAL = float(SEND_INTERVAL)
    COVERT_MESSAGE = os.environ.get('COVERT_MESSAGE', "ZXJyb3Itbm8tbXNn")
    print_host()
    try:
        COVERT_MESSAGE = base64.b64decode(COVERT_MESSAGE)
        pattern = convert_pattern(COVERT_MESSAGE, 256)
    except:
        print("ERROR: Unable to parse base64 covert message: {}".format(COVERT_MESSAGE))
        exit(1)
    print("Covert Message: {}".format(COVERT_MESSAGE))
    counter = 0
    first_byte = True
    while pattern:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((HOST, PORT))
                while pattern:
                    value = counter % 0xff
                    current = pattern[0]
                    s.send(counter.to_bytes(2, 'big') + b"\x00\x00\x00\x06\x01\x03\x00\x00\x00\x01")
                    if value == current:
                        s.send(counter.to_bytes(2, 'big') + b"\x00\x00\x00\x06\x01\x03\x00\x00\x00\x01")
                    counter += 1
                    if value == 0 and not first_byte:
                        pattern = pattern[1:]
                    first_byte = False
                    if pattern:
                        time.sleep(SEND_INTERVAL)
                s.close()
        except Exception as e:
            print(e, file=sys.stderr)
    print("done")
    exit(0)

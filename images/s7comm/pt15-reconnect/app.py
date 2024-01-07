import time
import socket
import os
import base64

from utilities import convert_pattern, print_host

if __name__ == '__main__':
    HOST = os.environ.get('TARGET_HOST', "google.com")  # The server's hostname or IP address
    PORT = os.environ.get('TARGET_PORT', 443)  # The port used by the server
    SEND_INTERVAL = float(os.environ.get('SEND_INTERVAL', 3))
    ADDITIONAL_INTERVAL = 0.05 # how many seconds to sleep aditional
    PORT = int(PORT)
    COVERT_MESSAGE = os.environ.get('COVERT_MESSAGE', "ZXJyb3Itbm8tbXNn")
    print_host()
    try:
        COVERT_MESSAGE = base64.b64decode(COVERT_MESSAGE)
        COVERT_MESSAGE = convert_pattern(COVERT_MESSAGE, 4)
    except:
        print("ERROR: Unable to parse base64 covert message: {}".format(COVERT_MESSAGE))
        exit(1)
    print("Covert Message: {}".format(COVERT_MESSAGE))
    while COVERT_MESSAGE:
        current = COVERT_MESSAGE[0]
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((HOST, PORT))
                s.close()
        except Exception as e:
            pass
        time.sleep(int(current) * SEND_INTERVAL)
        time.sleep(ADDITIONAL_INTERVAL * current)
        COVERT_MESSAGE = COVERT_MESSAGE[1:]
    print("done")
    exit(0)

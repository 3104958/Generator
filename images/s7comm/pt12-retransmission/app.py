import os
import random
import socket
import time
import ctypes
import base64
import dns.reversename, dns.resolver

import snap7
from snap7.types import Areas, S7DataItem, S7WLWord, S7WLReal, S7WLTimer
from snap7.util import set_int, set_real, get_int, get_real, get_s5time


from utilities import convert_pattern, print_host


def set_data_item(area, word_len, db_number: int, start: int, amount: int, data: bytearray) -> S7DataItem:
    item = S7DataItem()
    item.Area = ctypes.c_int32(area.value)
    item.WordLen = ctypes.c_int32(word_len)
    item.DBNumber = ctypes.c_int32(db_number)
    item.Start = ctypes.c_int32(start)
    item.Amount = ctypes.c_int32(amount)
    array_class = ctypes.c_uint8 * len(data)
    cdata = array_class.from_buffer_copy(data)
    item.pData = ctypes.cast(cdata, ctypes.POINTER(array_class)).contents
    return item

def get_my_service_name():
    service_name = None
    try:
        hostname = socket.gethostname()
        ip = socket.gethostbyname(hostname)
        reverse_entry = dns.reversename.from_address(ip)
        reverse_res = str(dns.resolver.resolve(reverse_entry, "PTR")[0])
        service_name = reverse_res.split('.', maxsplit=1)[0]
    except Exception as e:
        print(e)
        pass
    return service_name

if __name__ == "__main__":
    plc = snap7.client.Client()
    host = os.environ.get("TARGET_HOST", "172.17.0.2")
    server = socket.gethostbyname(host)
    port = int(os.environ.get("TARGET_PORT", 1102))
    replica = 1
    COVERT_MESSAGE = os.environ.get('COVERT_MESSAGE', "ZXJyb3Itbm8tbXNn")
    print_host()
    try:
        COVERT_MESSAGE = base64.b64decode(COVERT_MESSAGE)
        COVERT_MESSAGE = convert_pattern(COVERT_MESSAGE, 128)
    except Exception as e:
        print("unable to decode covert_message")
        COVERT_MESSAGE = []
    interval = float(os.environ.get("SEND_INTERVAL", 3.0))
    devices = int(os.environ.get('COVERT_VICTIMS', "0")) + 1
    my_index = replica * 4 + 8
    print("Connecting to {}:{}".format(server, port))
    plc.connect(server,  0, 1, port)
    count = 0
    while COVERT_MESSAGE:
        time.sleep(interval)
        current = COVERT_MESSAGE[0]
        replica = random.randrange(devices)
        my_index = replica * 4 + 8
        try:
            db_item = plc.db_read(1, my_index, 4)
            if current == count:
                count = 0
                db_item = plc.db_read(1, my_index, 4)
                COVERT_MESSAGE = COVERT_MESSAGE[1:]
            else:
                count += 1
            db_number = get_real(db_item, 0)
            print("received: {}".format( db_number))
        except Exception as e:
            print(e)
            print("... reconnecting")
            plc.disconnect()
            plc = snap7.client.Client()
            plc.connect(server, 0, 1, port)

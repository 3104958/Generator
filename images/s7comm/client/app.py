import os
import random
import socket
import time
import ctypes
import dns.reversename, dns.resolver

import snap7
from snap7.types import Areas, S7DataItem, S7WLWord, S7WLReal, S7WLTimer
from snap7.util import set_int, set_real, get_int, get_real, get_s5time




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
    replica = None
    try:
        service_name = get_my_service_name()
        print("my service_name is {}".format(service_name))
        replica = service_name.split('_')[-1]
        replica = int(replica)
    except Exception as e:
        print(e)
        replica = 0
    interval = float(os.environ.get("SEND_INTERVAL", 3.0))
    my_index = replica * 4 + 8
    print("I am service {} at index {}, sending every {} seconds".format(replica, my_index, interval))
    print("Connecting to {}:{}".format(server, port))
    plc.connect(server,  0, 1, port)
    while True:
        time.sleep(interval)
        try:
            number = random.uniform(2.7182818284, 3.141592)
            real = bytearray(4)
            set_real(real, 0, number)
            item = set_data_item(area=Areas.DB, word_len=S7WLReal, db_number=1, start=my_index, amount=1, data=real)
            plc.write_multi_vars([item,])
            db_item = plc.db_read(1, my_index, 4)
            db_number = get_real(db_item, 0)
            print("sent: {}, received: {}".format(number, db_number))
        except Exception as e:
            print(e)
            print("... reconnecting")
            plc.disconnect()
            plc = snap7.client.Client()
            plc.connect(server, 0, 1, port)

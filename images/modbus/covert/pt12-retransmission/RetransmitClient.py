import math
import os
import time

from TcpSession import TcpSession
from ClientInterface import ClientInterface
from scapy.all import send, sr1


class RetransmitClient(ClientInterface):
    _session : TcpSession = None
    _covert_data = b'secret'
    _current_bit = 0
    _finished = False
    _send_interval = float(os.environ.get("SEND_INTERVAL", 3.0))

    def _get_mask(self):
        return int(math.pow(2, self._current_bit))

    def should_manipulate(self) -> bool:
        current_byte = self._covert_data[0]
        current_mask = self._get_mask()
        self._current_bit += 1
        if self._current_bit == 8:
            self._current_bit = 0
            self._covert_data = self._covert_data[1:]
        return current_mask & current_byte != 0

    def send_proxy(self, data) -> None:
        if self.should_manipulate():
            send(data, verbose=0)
        send(data, verbose=0)

    def set_endpoint(self, host, port) -> None:
        self._session = TcpSession((host, port))


    def set_covert_data(self, data) -> None:
        self._covert_data = data

    def run(self):
        try:
            self._session.connect()
            counter = 1
            while not self._finished:
                current_frame = self._session.build(counter.to_bytes(2, 'big') + b"\x00\x00\x00\x06\x01\x03\x00\x00\x00\x01")
                self.send_proxy(current_frame)
                counter += 1
                if len(self._covert_data) == 0:
                    self._finished = True
                time.sleep(self._send_interval)
            self._session.close()
        except Exception as e:
            print("Exception: {}".format(e))

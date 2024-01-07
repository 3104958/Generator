from abc import ABC, abstractmethod


class ClientInterface(ABC):

    @abstractmethod
    def should_manipulate(self) -> bool:
        # decides if outgoing packets should be changed in order to covertly send data
        pass

    @abstractmethod
    def send_proxy(self, data) -> None:
        # the function intercepting packets - this is where the covert signal is modulated
        pass

    @abstractmethod
    def set_endpoint(self, host, port) -> None:
        # connect the Client to a server
        pass

    @abstractmethod
    def set_covert_data(self, data: bytes) -> None:
        # for the data that should be sent in the covert channel
        pass

    @abstractmethod
    def run(self):
        # the main loop that runs
        pass
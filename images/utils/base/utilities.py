import socket


def convert_pattern(message: bytes, divisor: int):
    """
    this function converts a message to a pattern of actions
    :param message a byte variable with the data to be converted
    :param divisor the number of actions that could be triggered later (in range [2..256]) 
    :return a list of actions
    """
    pattern = []
    while message:
        current = message[0]
        value = 1
        byte_pattern = []
        while value < 0x100:
            byte_pattern.append(current % divisor)
            current = int(current / divisor)
            value *= divisor
        byte_pattern.reverse()
        pattern += byte_pattern
        message = message[1:]
    return pattern


def print_host():
    """
    this function prints the current hostname as well as it's given ip (for analyzing the simulation data)
    :return None
    """
    try:
        hostname = socket.gethostname()
        ip = socket.gethostbyname(hostname)
        print("Host: {}, IP: {}".format(hostname, ip))
    except Exception as e:
        pass
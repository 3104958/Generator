from enum import Enum
from typing import Optional, Dict

from pydantic import BaseModel


class Channel(BaseModel):
    exploited_clients: int = 0
    path: Optional[str] = None
    covert_str: Optional[str] = None
    image: Optional[str] = None
    covert_file: Optional[str] = None


class ProtocolEnum(str, Enum):
    """
    a list of supported protocols and their corresponding folder
    @warning this parameter is case-sensitive
    """
    modbus = 'MODBUS'
    opcua = 'OPCUA'
    s7comm = 'S7COMM'
    mqtt = 'MQTT'
    coap = 'CoAP'


class Settings(BaseModel):
    time_quit: int
    name: Optional[str] = "unnamed-simulation"


class Server(BaseModel):
    host: str
    port: int
    internal: bool
    image: Optional[str] = None
    healthcheck: str
    path: Optional[str] = None


class Client(BaseModel):
    host: str
    instances: int
    image: Optional[str] = None
    path: Optional[str] = None


class Protocol(BaseModel):
    client: Client
    server: Server
    channels: Dict[str, Channel]
    time_interval: int


class ValidConfig(BaseModel):
    title: str
    owner: Dict
    settings: Settings
    protocols: Dict[ProtocolEnum, Protocol]

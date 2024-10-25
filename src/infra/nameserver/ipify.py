from ipaddress import IPv4Address
from requests import get

from src.infra.ip.interface import ExternalIpInterface

class Ipify(ExternalIpInterface):
    def get_ip(self) -> IPv4Address:
        
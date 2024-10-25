from abc import ABC, abstractmethod
from ipaddress import IPv4Address

class ExternalIpInterface(ABC):
    @abstractmethod
    def get_ip(self) -> IPv4Address:
        pass

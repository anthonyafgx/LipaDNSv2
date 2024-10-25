from abc import ABC, abstractmethod
from ipaddress import IPv4Address
from typing import Optional

from src.infra.loggers.interface import Logger

class ExternalIpInterface(ABC):
    @abstractmethod
    def get_ip(self, logger: Logger) -> Optional[IPv4Address]:
        pass

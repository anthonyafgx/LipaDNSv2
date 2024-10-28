from abc import ABC, abstractmethod
from ipaddress import IPv4Address
from typing import Optional

from src.domain.value_objects import DNSRecord
from src.infra.loggers.interface import Logger

class NameserverInterface(ABC):
    @abstractmethod
    def get_record_by_ip(self, ip: IPv4Address, logger: Logger) -> Optional[DNSRecord]:
        pass

    @abstractmethod
    def get_record_by_name(self, name: str, logger: Logger) -> Optional[DNSRecord]:
        pass

    @abstractmethod
    def set_record(self, dns_record: DNSRecord, logger: Logger):
        pass

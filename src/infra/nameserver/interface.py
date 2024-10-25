from abc import ABC, abstractmethod
from ipaddress import IPv4Address

from src.domain.value_objects import DNSRecord
from src.infra.loggers.interface import Logger

class NameserverInterface(ABC):
    @abstractmethod
    def get_record_by_ip(self, ip: IPv4Address, logger: Logger) -> DNSRecord:
        pass

    @abstractmethod
    def get_record_by_name(self, name: str, logger: Logger) -> DNSRecord:
        pass

    @abstractmethod
    def set_record(self, dns_record: DNSRecord, logger: Logger):
        pass

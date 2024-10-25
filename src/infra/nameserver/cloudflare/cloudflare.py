from ipaddress import IPv4Address

from src.infra.nameserver.interface import NameserverInterface
from src.domain.value_objects import DNSRecord
from src.infra.loggers.interface import Logger

class CloudflareNameserver(NameserverInterface):
    _cloudflare_api_key: str
    _cloudflare_zone_id: str

    def __init__(self, cloudflare_api_key: str, cloudflare_zone_id: str):
        self._cloudflare_api_key = cloudflare_api_key
        self._cloudflare_zone_id = cloudflare_zone_id

    def get_record_by_ip(self, ip: IPv4Address, logger: Logger) -> DNSRecord:
        pass

    def get_record_by_name(self, name: str, logger: Logger) -> DNSRecord:
        pass

    def set_record(self, dns_record: DNSRecord, logger: Logger):
        pass

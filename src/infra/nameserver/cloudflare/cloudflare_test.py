import pytest
import os
from dotenv import load_dotenv
from typing import Optional
from ipaddress import IPv4Address

from src.domain.value_objects import DNSRecord
from src.infra.nameserver.cloudflare.cloudflare import CloudflareNameserver
from src.infra.loggers.standard import Logger, StandardLogger, LogLevel

def test_get_record_by_ip():
    logger: Logger = StandardLogger(LogLevel.DEBUG)
    api_key: str = os.getenv('CLOUDFLARE_API_KEY', '')
    cloudflare_zone_id: str = os.getenv('CLOUDFLARE_ZONE_ID', '')
    nameserver = CloudflareNameserver(cloudflare_api_key=api_key, cloudflare_zone_id=cloudflare_zone_id)

    dns_record: Optional[DNSRecord] = nameserver.get_record_by_ip(
                                        ip=IPv4Address(""), 
                                        logger=logger)
    
    assert dns_record
    assert dns_record.name == "" 

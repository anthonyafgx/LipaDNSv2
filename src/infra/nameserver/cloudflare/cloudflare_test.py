import pytest
import os
from dotenv import load_dotenv
from typing import Optional
from ipaddress import IPv4Address

from src.domain.value_objects import DNSRecord
from src.infra.nameserver.cloudflare.cloudflare import CloudflareNameserver
from src.infra.loggers.standard import Logger, StandardLogger, LogLevel

load_dotenv('.testenv')

@pytest.fixture
def api_key() -> str:
    return os.getenv('CLOUDFLARE_API_KEY', '')

@pytest.fixture
def cloudflare_zone_id() -> str:
    return os.getenv('CLOUDFLARE_ZONE_ID', '')

@pytest.fixture
def domain_name() -> str:
    return os.getenv('DOMAIN_NAME', '')

@pytest.fixture
def test_ip() -> str:
    return os.getenv('TEST_IP', '')

def test_get_record_by_ip(api_key: str, cloudflare_zone_id: str, domain_name: str, test_ip: str): # type: ignore
    logger: Logger = StandardLogger(LogLevel.INFO)
    nameserver = CloudflareNameserver(cloudflare_api_key=api_key, cloudflare_zone_id=cloudflare_zone_id)
    dns_record: Optional[DNSRecord] = nameserver.get_record_by_ip(
                                        ip=IPv4Address(test_ip),
                                        logger=logger)
    
    assert dns_record
    assert dns_record.name == domain_name

def test_set_record(api_key: str, cloudflare_zone_id: str, domain_name: str, test_ip: str): # type: ignore
    logger: Logger = StandardLogger(LogLevel.INFO)
    nameserver = CloudflareNameserver(cloudflare_api_key=api_key, cloudflare_zone_id=cloudflare_zone_id)
    dns_record = DNSRecord(ip=IPv4Address(test_ip), name=domain_name)
    
    nameserver.set_record(dns_record=dns_record, logger=logger)

    assert nameserver.get_record_by_ip(test_ip, logger) == dns_record
    assert nameserver.get_record_by_name(domain_name, logger) == dns_record

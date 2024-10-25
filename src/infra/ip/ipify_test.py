import pytest
from ipaddress import IPv4Address

from src.infra.ip.ipify import Ipify
from src.infra.loggers.standard import StandardLogger, LogLevel

def test_get_ip_success():
    ipify = Ipify()
    logger = StandardLogger(LogLevel.INFO)
    ip: IPv4Address | None = ipify.get_ip(logger)
    
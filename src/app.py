import os
import sys
import asyncio
from dotenv import load_dotenv
from typing import Optional

from src.infra.ip.interface import ExternalIpInterface
from src.infra.nameserver.interface import NameserverInterface
from src.infra.loggers.interface import Logger
from src.infra.ip.ipify import Ipify
from src.infra.nameserver.cloudflare.cloudflare import CloudflareNameserver
from src.infra.loggers.standard import StandardLogger, LogLevel

from src.services.services import refresh_service

async def refresh_service_task(external_ip_service: ExternalIpInterface, nameserver: NameserverInterface, domain_name: str, refresh_rate: int, logger: Logger):
    """
    Runs the DNS synchronization task asynchronously, refreshing at the specified interval.
    """
    while True:
        refresh_service(external_ip_service, nameserver, domain_name, logger)
        await asyncio.sleep(refresh_rate)

async def main():
    """
    Initialize dependencies
    """
    load_dotenv()
    logger = StandardLogger(log_level=LogLevel.INFO)
    
    DOMAIN_NAME: Optional[str] = os.getenv("DOMAIN_NAME")
    CLOUDFLARE_API_TOKEN: Optional[str] = os.getenv("CLOUDFLARE_API_TOKEN")
    CLOUDFLARE_ZONE_ID: Optional[str] = os.getenv("CLOUDFLARE_ZONE_ID")
    REFRESH_RATE: Optional[int] = int(os.getenv("REFRESH_RATE", "0"))
    try:
        if CLOUDFLARE_API_TOKEN is None:
            raise ValueError("Environment variable 'CLOUDFLARE_API_TOKEN' cannot be None")
        if CLOUDFLARE_ZONE_ID is None:
            raise ValueError("Environment variable 'CLOUDFLARE_ZONE_ID' cannot be None")
        if DOMAIN_NAME is None:
            raise ValueError("Environment variable 'DOMAIN_NAME' cannot be None")
        if REFRESH_RATE == 0:
            raise ValueError("Environment variable 'REFRESH_RATE' cannot be 0")
    except ValueError as e:
        logger.critical(f"{e}")
        sys.exit(1)

    ip_service = Ipify()
    nameserver = CloudflareNameserver(cloudflare_api_key=CLOUDFLARE_API_TOKEN, 
                                      cloudflare_zone_id=CLOUDFLARE_ZONE_ID)
    
    await refresh_service_task(external_ip_service=ip_service,
                               nameserver=nameserver,
                               domain_name=DOMAIN_NAME,
                               refresh_rate=REFRESH_RATE,
                               logger=logger)

if __name__ == '__main__':
    asyncio.run(main())

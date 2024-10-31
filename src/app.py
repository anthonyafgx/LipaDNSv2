import os
import asyncio
from dotenv import load_dotenv
from typing import Optional

from src.infra.ip.ipify import Ipify
from src.infra.nameserver.cloudflare.cloudflare import CloudflareNameserver
from src.infra.loggers.standard import StandardLogger, LogLevel

from src.services.services import refresh_service

def main():
    load_dotenv()
    DOMAIN_NAME: Optional[str] = os.getenv("DOMAIN_NAME")
    CLOUDFLARE_API_KEY: Optional[str] = os.getenv("CLOUDFLARE_API_TOKEN")
    CLOUDFLARE_ZONE_ID: Optional[str] = os.getenv("CLOUDFLARE_ZONE_ID")
    logger = StandardLogger(log_level=LogLevel.INFO)
    ip_service = Ipify()
    nameserver = CloudflareNameserver(cloudflare_api_key=CLOUDFLARE_API_KEY, 
                                      cloudflare_zone_id=CLOUDFLARE_ZONE_ID)

if __name__ == '__main__':
    main()

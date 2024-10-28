from requests import get, Response, RequestException, ConnectionError, HTTPError, Timeout
from ipaddress import IPv4Address
from typing import Optional

from src.infra.nameserver.interface import NameserverInterface
from src.domain.value_objects import DNSRecord
from src.infra.loggers.interface import Logger
from src.infra.nameserver.cloudflare.dtos import CloudflareListDNSRecordsInputDTO, CloudflareDNSRecord

class CloudflareNameserver(NameserverInterface):
    _cloudflare_api_key: str
    _cloudflare_zone_id: str

    def __init__(self, cloudflare_api_key: str, cloudflare_zone_id: str):
        self._cloudflare_api_key = cloudflare_api_key
        self._cloudflare_zone_id = cloudflare_zone_id

    def get_record_by_ip(self, ip: IPv4Address, logger: Logger) -> Optional[DNSRecord]:
        params: dict[str, str | IPv4Address] = {
            "content": ip,
            "type": "A" # IPv4
        }

        return self._get_record(params=params, logger=logger)

    def get_record_by_name(self, name: str, logger: Logger) -> Optional[DNSRecord]:
        params: dict[str, str | IPv4Address] = {
            "content": name,
            "type": "A" # IPv4
        }

        return self._get_record(params=params, logger=logger)

    def set_record(self, dns_record: DNSRecord, logger: Logger):
        pass

    def _get_record(self, params: dict[str, str | IPv4Address], logger: Logger):
        url: str = f"https://api.cloudflare.com/client/v4/zones/{self._cloudflare_zone_id}/dns_records"
        
        headers = {
            "Content-Type": "application/json",
            "X-Auth-Key": self._cloudflare_api_key
        }
        
        # Make request to Cloudflare
        response = Response()
        try:
            response = get(url=url, headers=headers, params=params, timeout=5) # type: ignore
            response.raise_for_status()
            logger.info(f"Successfully fetched the DNS Record from Cloudflare. Parameters: {params}")
        except ConnectionError as e:
            logger.error(f"Connection Error. Failed to connect to the Cloudflare API: {e.response}")
            return None
        except HTTPError as e:
            logger.error(f"HTTP Error. Invalid HTTP Response: {e.response}")
            return None
        except Timeout:
            logger.error(f"Request timed out when fetching the DNS Record from Cloudflare. Parameters: {params}")
            return None
        except RequestException as e:
            logger.error(f"An error occurred during the request {e}")
            return None

        # Unpack json and return
        try:
            input_dto = CloudflareListDNSRecordsInputDTO(**response.json())
            dns_record: CloudflareDNSRecord = input_dto.result[0]
            return DNSRecord(name=dns_record.name, ip=dns_record.content)
        except ValueError as e:
            logger.error(f"Failed to parse request JSON: {e}")
            return None
        
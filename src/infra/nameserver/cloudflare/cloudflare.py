from ipaddress import IPv4Address
from typing import Optional
from requests import get, post, patch, Response, RequestException, ConnectionError, HTTPError, Timeout

from src.domain.value_objects import DNSRecord
from src.infra.loggers.interface import Logger
from src.infra.nameserver.interface import NameserverInterface
from src.infra.nameserver.cloudflare.dtos import CloudflareListDNSRecordsInputDTO, CloudflareDNSRecordInputDTO, CloudflareDNSRecordOutputDTO
from src.infra.nameserver.cloudflare.exceptions import MultipleDNSRecordsFoundError

class CloudflareNameserver(NameserverInterface):
    _cloudflare_api_key: str
    _cloudflare_zone_id: str
    _headers: dict[str, str]

    def __init__(self, cloudflare_api_key: str, cloudflare_zone_id: str):
        self._cloudflare_api_key = cloudflare_api_key
        self._cloudflare_zone_id = cloudflare_zone_id
        self._headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self._cloudflare_api_key}"
        }

    def get_record_by_ip(self, ip: IPv4Address, logger: Logger) -> Optional[DNSRecord]:
        params: dict[str, str | IPv4Address] = {
            "content": ip,
            "type": "A" # IPv4
        }

        cloudflare_dns_record: Optional[CloudflareDNSRecordInputDTO] = self._get_cloudflare_record(params=params, logger=logger)

        if (cloudflare_dns_record is None):
            return None

        return DNSRecord(ip=cloudflare_dns_record.content,
                         name=cloudflare_dns_record.name)

    def get_record_by_name(self, name: str, logger: Logger) -> Optional[DNSRecord]:
        params: dict[str, str | IPv4Address] = {
            "name": name,
            "type": "A" # IPv4
        }

        cloudflare_dns_record: Optional[CloudflareDNSRecordInputDTO] = self._get_cloudflare_record(params=params, logger=logger)

        if (cloudflare_dns_record is None):
            return None

        return DNSRecord(ip=cloudflare_dns_record.content,
                         name=cloudflare_dns_record.name)

    def set_record(self, dns_record: DNSRecord, logger: Logger):
        lookup_information: dict[str, str | IPv4Address] = {
            "name": dns_record.name,
            "type": "A" # IPv4
        }

        existing_record: Optional[CloudflareDNSRecordInputDTO] = self._get_cloudflare_record(params=lookup_information, logger=logger)

        if (existing_record is None):
            # If record does not exist, create it
            output_dto = CloudflareDNSRecordOutputDTO(
                name=dns_record.name,
                content=dns_record.ip,
            )

            url: str = f"https://api.cloudflare.com/client/v4/zones/{self._cloudflare_zone_id}/dns_records"
            try:
                response = post(url=url, headers=self._headers, json=output_dto.model_dump(), timeout=5)
                response.raise_for_status()
                logger.info(f"Successfully created the Cloudflare DNS Record with params: {output_dto.model_dump()}")
            except ConnectionError as e:
                logger.error(f"Connection Error. Failed to connect to the Cloudflare API: {e.response}")
                return
            except HTTPError as e:
                logger.error(f"HTTP Error [Status code {e.response.status_code}]. Invalid HTTP Response: {e.response.json()}.\nRequest URL: {e.request.url}\nRequest body: {e.request.body}")
                return
            except Timeout:
                logger.error("Request timed out when fetching the DNS Record from Cloudflare")
                return
            except RequestException as e:
                logger.error(f"An error occurred during the request {e.response}")
                return
        else:
            # If exists, update it
            url: str = f"https://api.cloudflare.com/client/v4/zones/{self._cloudflare_zone_id}/dns_records/{existing_record.id}"
            patch_information: dict[str, str | bool] = {}
            patch_information.update(lookup_information) # type: ignore
            patch_information["content"] = str(dns_record.ip)
            patch_information["proxied"] = True

            try:
                patch(url=url, headers=self._headers, json=patch_information, timeout=5)
            except ConnectionError as e:
                logger.error(f"Connection Error. Failed to connect to the Cloudflare API: {e.response}")
                return
            except HTTPError as e:
                logger.error(f"HTTP Error. Invalid HTTP Response: {e.response}")
                return
            except Timeout:
                logger.error("Request timed out when fetching the DNS Record from Cloudflare")
                return
            except RequestException as e:
                logger.error(f"An error occurred during the request {e.response}")
                return


    def _get_cloudflare_record(self, params: dict[str, str | IPv4Address], logger: Logger) -> Optional[CloudflareDNSRecordInputDTO]:
        url: str = f"https://api.cloudflare.com/client/v4/zones/{self._cloudflare_zone_id}/dns_records"
        
        # Make request to Cloudflare
        response = Response()
        try:
            response = get(url=url, headers=self._headers, params=params, timeout=5) # type: ignore
            response.raise_for_status()
            logger.info(f"Successfully fetched the DNS Record from Cloudflare. Parameters: {params}")
        except ConnectionError as e:
            logger.error(f"Connection Error. Failed to connect to the Cloudflare API: {e.response}")
            return None
        except HTTPError as e:
            logger.error(f"HTTP Error [Status code {e.response.status_code}]. Invalid HTTP Response: {e.response.json()}")
            return None
        except Timeout:
            logger.error(f"Request timed out when fetching the DNS Record from Cloudflare. Parameters: {params}")
            return None
        except RequestException as e:
            logger.error(f"An error occurred during the request {e.response}")
            return None

        # Unpack json and return
        try:
            input_dto = CloudflareListDNSRecordsInputDTO(**response.json())
            if (input_dto.result_info.count == 0):
                logger.warning(f"No Cloudflare DNS record found for params: {params}")
                return None
            if (input_dto.result_info.count > 1):
                raise MultipleDNSRecordsFoundError(input_dto=input_dto)
            cloudflare_dns_record: CloudflareDNSRecordInputDTO = input_dto.result[0]
            logger.info(f"Cloudflare DNS record found for params: {params}")
            return cloudflare_dns_record
        except ValueError as e:
            logger.error(f"Failed to parse request JSON: {e}")
            return None
        except MultipleDNSRecordsFoundError as e:
            logger.error(f"Failed to process JSON: {e}")
            return None
        
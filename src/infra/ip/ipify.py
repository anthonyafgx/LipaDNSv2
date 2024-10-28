from ipaddress import IPv4Address, AddressValueError
from requests import get, Response, RequestException, Timeout
from typing import Optional

from src.infra.ip.interface import ExternalIpInterface
from src.infra.loggers.interface import Logger

class Ipify(ExternalIpInterface):
    def get_ip(self, logger: Logger) -> Optional[IPv4Address]:
        response: Response = Response()
        try:
            response = get('https://api.ipify.org', timeout=5)
            ip: IPv4Address = IPv4Address(response.text)
            logger.info(f"Successfully fetched IP from Ipify: {ip}")
            return ip
        except Timeout:
            logger.error("Request timed out when fetching the IP from Ipify.")
            return None
        except AddressValueError:
            logger.error(f"Received an invalid IPv4 address from Ipify: {response.text}")
            return None
        except RequestException as e:
            logger.error(f"An error occurred during the request {e}")
            return None
        
from ipaddress import IPv4Address
from typing import Optional

from src.domain.value_objects import DNSRecord

from src.infra.ip.interface import ExternalIpInterface
from src.infra.nameserver.interface import NameserverInterface
from src.infra.loggers.interface import Logger

def refresh_service(external_ip_service: ExternalIpInterface, nameserver: NameserverInterface, domain_name: str, logger: Logger):
    """
    Checks if the external IP address has changed, and if so, updates the DNS record accordingly.

    This function interacts with two main services:
    1. `external_ip_service`: Obtains the current external IP address.
    2. `nameserver`: Manages DNS records for a specified domain.

    The function performs the following steps:
    - Fetches the external IP address using `external_ip_service`.
    - Retrieves the current DNS record associated with `domain_name`.
    - Compares the external IP address with the IP in the DNS record.
    - If the IPs differ, it updates the DNS record with the new external IP.
    - Logs each step and result for troubleshooting and monitoring purposes.

    Arguments:
        external_ip_service (ExternalIpInterface): Service used to retrieve the current external IP address.
        nameserver (NameserverInterface): Service used to manage DNS records for the domain.
        domain_name (str): The domain name whose DNS record should be updated if needed.
        logger (Logger): Logger instance for recording operations and errors.

    Returns:
        None: This function does not return any value; it logs the process and updates the DNS if necessary.

    Raises:
        If the external IP cannot be obtained or the DNS record is not found, logs critical errors and exits the function.
    """

    external_ip: Optional[IPv4Address] = external_ip_service.get_ip(logger)
    if external_ip is None:
        logger.critical("Could not obtain a valid IP address from the External IP Service")
        return
    
    current_dns_record: Optional[DNSRecord] = nameserver.get_record_by_name(name=domain_name, logger=logger)
    if current_dns_record is None:
        logger.critical("Could not obtain the current DNS record")
        return
    
    if external_ip != current_dns_record.ip:
        nameserver.set_record(dns_record=DNSRecord(ip=external_ip, name=domain_name), logger=logger)
        logger.info(f"External IP changed. Successfully changed the content of the DNS Record {current_dns_record.name} to {external_ip}")
        return
    
    logger.debug("Refresh service ran. No external IP change detected.")

from pydantic import BaseModel, Field, ConfigDict
from ipaddress import IPv4Address

class DNSRecord(BaseModel):
    model_config = ConfigDict(frozen=True)

    ip: IPv4Address = Field(..., description="IP address associated with the DNS Record")
    name: str = Field(..., max_length=255, description="The name of the DNS Record")

class IPAddress(BaseModel):
    model_config = ConfigDict(frozen=True)
    externalIp: IPv4Address = Field(..., description="IP address of the server as seen from an specific external element")
    nameserverIp: IPv4Address = Field(..., description="IP address of the server according to the nameserver")
    
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Dict
from ipaddress import IPv4Address

class CloudflareDNSRecord(BaseModel):
    model_config = ConfigDict(frozen=True)

    id: str
    name: str
    content: IPv4Address

class CloudflareMessage(BaseModel):
    model_config = ConfigDict(frozen=True)

    code: int = Field(..., gt=0, le=1000)
    message: str

class CloudflareResultInfo(BaseModel):
    model_config = ConfigDict(frozen=True)

    count: int = Field(..., ge=0)
    page: int = Field(..., ge=0)
    per_page: int = Field(..., ge=0)
    total_count: int = Field(..., ge=0)

class CloudflareListDNSRecordsInputDTO(BaseModel):
    """"
    https://developers.cloudflare.com/api/operations/dns-records-for-a-zone-list-dns-records
    """
    model_config = ConfigDict(frozen=True)

    success: bool
    errors: list[CloudflareMessage] = Field(default_factory=list)
    messages: list[CloudflareMessage] = Field(default_factory=list)
    result_info: CloudflareResultInfo
    result: list[CloudflareDNSRecord]

class CloudflareListDNSRecordsOutputDTO(BaseModel):
    """"
    https://developers.cloudflare.com/api/operations/dns-records-for-a-zone-list-dns-records
    """
    model_config = ConfigDict(frozen=True)

    content: Optional[IPv4Address] = None
    name: Optional[str] = None
    type: str = Field(default="A", frozen=True) # IPv4

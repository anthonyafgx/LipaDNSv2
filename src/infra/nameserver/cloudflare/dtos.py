from pydantic import BaseModel, Field, ConfigDict, field_serializer
from typing import Optional
from ipaddress import IPv4Address

class CloudflareDNSRecordInputDTO(BaseModel):
    model_config = ConfigDict(frozen=True)

    id: str
    name: str
    content: IPv4Address

class CloudflareDNSRecordOutputDTO(BaseModel):
    id: Optional[str] = None
    """Only required when updating record, not for creating it"""
    name: str = Field(min_length=1, max_length=255)
    """DNS Record Name (or @ for the zone apex) in Punycode"""
    content: IPv4Address
    """Content of the DNS Record"""
    proxied: Optional[bool] = Field(default=True)
    """Whether the record is proxied by Cloudflare."""
    comment: str = Field(default="This is a record managed by LipaDNSv2, a DDNS service.")
    type: str = Field(default="A", frozen=True)

    @field_serializer('content')
    def serialize_content(self, content: IPv4Address, _info):
        """Converts the IPv4 to a string, so it can be serialized to a JSON object"""
        return str(content)

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
    result: list[CloudflareDNSRecordInputDTO]
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Dict
from ipaddress import IPv4Address

class CloudflareDNSRecordDTO(BaseModel):
    model_config = ConfigDict(frozen=True)

    id: str
    name: str
    content: IPv4Address

class CloudflareMessageDTO(BaseModel):
    model_config = ConfigDict(frozen=True)

    code: int = Field(..., gt=0, le=1000)
    message: str

class CloudflareResultInfoDTO(BaseModel):
    model_config = ConfigDict(frozen=True)

    count: int = Field(..., ge=0)
    page: int = Field(..., ge=0)
    per_page: int = Field(..., ge=0)
    total_count: int = Field(..., ge=0) 

class CloudflareListDNSRecordsDTO(BaseModel):
    model_config = ConfigDict(frozen=True)

    success: bool
    errors: list[CloudflareMessageDTO] = Field(default_factory=list)
    messages: list[CloudflareMessageDTO] = Field(default_factory=list)
    result_info: CloudflareResultInfoDTO
    result: list[CloudflareDNSRecordDTO]

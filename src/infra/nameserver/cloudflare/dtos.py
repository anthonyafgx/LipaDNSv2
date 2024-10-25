from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Dict

class CloudflareDNSRecord(BaseModel):
    id: str
    type: str
    name: str
    content: str
    proxiable: bool
    proxied: bool
    ttl: int
    locked: bool
    zone_id: str
    zone_name: str
    created_on: str
    modified_on: str
    data: Optional[dict] = Field(default_factory=dict)

from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Article:
    external_id: str
    title: str
    summary: str
    link: str
    content: str
    published_at: datetime

    source_domain: str
    source_name: str
    published_at: Optional[datetime]
    created_at: datetime

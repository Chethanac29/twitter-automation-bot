from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Article:
    id: Optional[int] = None
    external_id: str = ""
    title: str = ""
    summary: str = ""
    content: str = ""
    link: str = ""
    source_domain: str = ""
    source_name: str = ""
    published_at: Optional[datetime] = None
    created_at: Optional[datetime] = None
    is_processed: bool = False
    processed_at: Optional[datetime] = None


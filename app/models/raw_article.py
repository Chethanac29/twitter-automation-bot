from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class RawArticle:
    id: Optional[int] = None
    external_id: str = ""
    title: str = ""
    summary: str = ""
    link: str = ""
    published_at: Optional[datetime] = None
    source: str = ""
    created_at: Optional[datetime] = None
    is_scraped: bool = False
    scrape_status: str = "pending"
    is_built: bool = False
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Tweet:
    id: Optional[int] = None
    article_id: int = 0
    tweet_text: str = ""
    platform: str = "threads"
    status: str = "pending"
    created_at: Optional[datetime] = None
    posted_at: Optional[datetime] = None
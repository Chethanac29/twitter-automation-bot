from dataclasses import dataclass
from datetime import datetime
from typing import List

@dataclass
class Tweet:
    tweet_text: str
    category: str
    hash_tags: List[str]
    created_at: datetime
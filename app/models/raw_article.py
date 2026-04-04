from dataclasses import dataclass
from datetime import datetime

@dataclass
class RawArticle:
    external_id : str
    title : str
    summary : str
    link : str
    published_at : datetime
    source : str

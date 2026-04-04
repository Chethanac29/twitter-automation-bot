import feedparser
from typing import List
from models.raw_article import RawArticle
from datetime import datetime, timezone
from urllib.parse import urlparse
def fetch_rss_articles(rss_feeds: List[str]) -> List[RawArticle]:
    raw_articles = []

    for url in rss_feeds:
        feed = feedparser.parse(url)

        for entry in feed.entries:
            
            title = entry.get("title", "")
            summary = entry.get("summary", "")
            link = entry.get("link", "")
            external_id = entry.get("guid") or link.split("?")[0] # Use guid if available, otherwise use the link without query parameters as a fallback
            published_at = entry.get("published_parsed") #or entry.get("updated_parsed") #autocomplete
            if published_at:
                published_at = datetime(*published_at[:6],tzinfo=timezone.utc) # Convert to datetime object with timezone info (UTC in this case)
            else:
                published_at = datetime.now() # fallback to current time if not available

            source = urlparse(url).netloc # Extract the domain name as the source

            raw_article = RawArticle(
                external_id = external_id,
                title = title,
                summary = summary,
                link = link,
                published_at = published_at,
                source = source
            )
            raw_articles.append(raw_article)
    return raw_articles
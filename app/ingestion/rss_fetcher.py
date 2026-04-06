import re
import feedparser
from typing import List
from datetime import datetime, timedelta, timezone
from urllib.parse import urlparse

from app.models.raw_article import RawArticle
from app.utils.logger import get_logger

logger = get_logger(__name__)


def clean_html(text: str) -> str:
    """
    Remove basic HTML tags from RSS summary text.
    """
    if not text:
        return ""
    return re.sub(r"<[^>]+>", "", text).strip()


def fetch_rss_articles(rss_feeds: List[str]) -> List[RawArticle]:
    """
    Fetch raw articles from a list of RSS feeds.
    """
    raw_articles = []

    for url in rss_feeds:
        logger.info(f"Fetching RSS feed: {url}")

        try:
            feed = feedparser.parse(url)

            if getattr(feed, "bozo", False):
                logger.warning(f"RSS parsing warning for {url}: {getattr(feed, 'bozo_exception', 'Unknown issue')}")

            for entry in feed.entries:
                title = (entry.get("title") or "").strip()
                summary = clean_html((entry.get("summary") or "").strip())
                link = (entry.get("link") or "").strip()

                if not link:
                    logger.warning(f"Skipping RSS entry with missing link from feed: {url}")
                    continue

                external_id = (entry.get("guid") or link.split("?")[0]).strip()

                published_struct = entry.get("published_parsed") or entry.get("updated_parsed")
                if published_struct:
                    published_at = datetime(*published_struct[:6], tzinfo=timezone.utc)
                else:
                    published_at = datetime.now(timezone.utc)

                source = urlparse(url).netloc

                today = datetime.now(timezone.utc)

                # skip stale articles older than 10 days
                if published_at.date() < (today.date() - timedelta(days=10)):
                    logger.info(
                        f"Skipping old article: {title or '[No Title]'} | published_at: {published_at}"
                    )
                    continue

                raw_article = RawArticle(
                    external_id=external_id,
                    title=title,
                    summary=summary,
                    link=link,
                    published_at=published_at,
                    source=source
                )

                raw_articles.append(raw_article)

        except Exception as e:
            logger.exception(f"Failed to fetch or parse RSS feed {url}: {e}")

    logger.info(f"Fetched total {len(raw_articles)} raw articles from RSS feeds.")

    return raw_articles
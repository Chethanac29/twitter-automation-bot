from newspaper import Article as NewspaperArticle
from typing import Optional, List

from app.models.article import Article
from app.db.article_repository import insert_articles
from app.db.raw_articles_repository import update_scrape_status
from app.utils.logger import get_logger
from app.models.raw_article import RawArticle

logger = get_logger(__name__)


def scrape_artcile_content(raw_article: RawArticle) -> str:
    """
    Scrape article content from the given raw article link.
    Falls back to summary if scraping fails or content is empty.
    Also updates scrape status in the database.
    """
    logger.info(f"Scraping the article: {raw_article.title} from {raw_article.link}")
    fallback_content = f"{raw_article.title}\n\n{raw_article.summary}"
    content = scrape_article(raw_article.link)

    if content:
        update_scrape_status(
            article_id=raw_article.id, is_scraped=True, scrape_status="success"
        )
        logger.info(f"Scraping succesful for article: {raw_article.id}")
        return content

    logger.warning(
        f"Scraping failed for article: {raw_article.id}. Falling back to summary."
    )
    update_scrape_status(
        article_id=raw_article.id, is_scraped=True, scrape_status="failed"
    )
    return fallback_content


def scrape_article(link: str) -> Optional[str]:
    """
    Scrape article content from the given article link.
    return the content if successful
    """
    try:
        article = NewspaperArticle(link)
        article.config.browser_user_agent = (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        )
        article.download()
        article.parse()

        content = article.text

        if not content or len(content.strip()) < 10:
            print(f"Warning: No content found for {link}")
            return None

        return content.strip()
    except Exception as e:
        logger.exception(f"Error scraping article at {link}: {e}")
        return None

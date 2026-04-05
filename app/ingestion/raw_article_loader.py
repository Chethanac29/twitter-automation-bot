from typing import List

from app.ingestion.rss_fetcher import fetch_rss_articles
from app.db.raw_articles_repository import insert_raw_articles
from app.models.raw_article import RawArticle
from app.utils.logger import get_logger

logger = get_logger(__name__)

def load_raw_articles(rss_feeds: List[str]) -> int:
    '''Fetch rss feeds and load new articles to the database'''
    logger.info('Starting th raw article ingestion.....')


    #step 1 fetche from rss

    try:
        raw_articles: List[RawArticle] = fetch_rss_articles(rss_feeds)
        logger.info(f"Fetched {len(raw_articles)} articles")
        raw_articles = deduplicate_articles(raw_articles)
        logger.info(f"{len(raw_articles)} articles after deduplication.")

    except Exception as e:
        logger.error(f"Failed to fetch articles: {e}")
        raise

    if not raw_articles:
        logger.info('No articles found. exiting ingestion....')
        return 0
    

    # step 2: inserting the raw articles into the database

    try:
        inserted_count = insert_raw_articles(raw_articles)
        logger.info(f'Inserted {inserted_count} new articles into the database.')
        return inserted_count
    except Exception as e:
        logger.error(f"Failed to insert articles: {e}")
        raise


def deduplicate_articles(raw_articles: List[RawArticle]) -> List[RawArticle]:
    '''Deduplicate the raw articles based on their external_id'''
    seen = set()
    deduplicated = []
    for article in raw_articles:
        external_id = article.external_id.strip() if article.external_id else article.external_id
        if external_id not in seen:
            seen.add(external_id)
            deduplicated.append(article)
    return deduplicated



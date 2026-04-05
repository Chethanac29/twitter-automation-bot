from typing import List
from psycopg2.extras import execute_values

from app.db.connection import get_connection
from app.models.article import Article
from app.utils.logger import get_logger

logger = get_logger(__name__)

# Insert articles into the database

def insert_articles(articles: list[Article]) -> int:
    '''Insert articles into the databse and  return the number of Articles inserted'''

    if not articles:
        logger.info('No articles to insert.')
        return 0

    logger.info(f'Inserting {len(articles)} articles into the database...')

    insert_query = '''
        INSERT INTO articles (
        external_id,
        title,
        summary,
        content,
        link,
        source_domain,
        source_name,
        published_at
        )
        VALURES %s
        ON CONFLICT (external_id) DO NOTHING
        '''
    values = [
        (
            article.external_id,
            article.title,
            article.summary,
            article.content,
            article.link,
            article.source_domain,
            article.source_name,
            article.published_at
        ) for article in articles
    ]

    conn = get_connection()
    cursor = conn.cursor()

    try:
        execute_values(cursor, insert_query, values)
        conn.commit()
        logger.info(f'Attempted to insert {len(articles)} canonical articles into the database.')
        return len(articles)
    except Exception as e:
        conn.rollback()
        logger.exception(f"Error in inserting the canonical articles: {e}")
        raise
    finally:
        cursor.close()
        conn.close()

    
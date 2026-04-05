import psycopg2
from psycopg2.extras import execute_values
from typing import List
from app.db.connection import get_connection
from app.models.raw_article import RawArticle
from app.utils.logger import get_logger

logger = get_logger(__name__)


# INSERT RAW ARTICLES INTO THE DATABASE
def insert_raw_articles(raw_articles: List[RawArticle]) -> int:
    """
    Inset raw articles into the database and igonrin the duplicated ones.
    return the number if rows inserted.
    """

    if not raw_articles:
        logger.info("No raw articles to insert.")
        return 0

    logger.info(f"Inserting {len(raw_articles)} raw articles into the database.")

    query = """
            INSERT INTO raw_articles(
            external_id,
            title,
            summary,
            link,
            published_at,
            source
            )
            VALUES %s
            ON CONFLICT (external_id) DO NOTHING;
            """
    values = [
        (
            article.external_id,
            article.title,
            article.summary,
            article.link,
            article.published_at,
            article.source,
        )
        for article in raw_articles
    ]
    conn = get_connection()
    cursor = conn.cursor()

    try:
        execute_values(cursor, query, values)
        conn.commit()
        logger.info(f"Inseted {len(values)} raw articles into the database.")
        return len(values)
    except Exception as e:
        conn.rollback()
        logger.exception(f"Error Inserting the raw articles into the databas")
        raise 
    finally:
        cursor.close()
        conn.close()


def fetch_unbuilt_raw_articles(limit: int = 100) -> List[RawArticle]:
    """fetch the raw-articles that are not yet processed in build pipeline"""
    logger.info("Fetching unbuilt raw-articles from the database")

    query = """
    SELECT
        id,
        external_id,
        title,
        summary,
        link,
        published_at,
        source
    FROM raw_articles
    WHERE is_built = FALSE
    order by published_at DESC
    LIMIT %s;
    """
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(query, (limit,))
        rows = cursor.fetchall()
        logger.info(f"Fetched {len(rows)} unbuilt raw-articles from the database")
        articles = []
        for row in rows:
            articles.append(
                RawArticle(
                    id=row[0],
                    external_id=row[1],
                    title=row[2],
                    summary=row[3],
                    link=row[4],
                    published_at=row[5],
                    source=row[6],
                )
            )
        return articles
    except Exception as e:
        logger.exception(f"Error fetching raw articles: {e}")
        raise
    finally:
        cursor.close()
        conn.close()


def update_scrape_status(article_id: int, is_scraped: bool, scrape_status: str):
    """Updating the scraping status of the article"""
    logger.info(f"Updating scraping status for article id: {article_id}")

    query = """
        UPDATE raw_articles 
        SET 
            is_scraped = %s,
            scrape_status = %s 
        WHERE id = %s;
    """
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(query, (is_scraped, scrape_status, article_id))
        conn.commit()
        logger.info(f"Scraping status updated successfully for article id: {article_id}")
    except Exception as e:
        logger.exception(
            f"Error updating scraping status for article id: {article_id}: {e}"
        )
        raise
    finally:
        cursor.close()
        conn.close()


def mark_articles_as_built(article_ids: List[int]):
    """Mark artilces as processed in build pipeline"""

    if not article_ids:
        return
    logger.info("Marking articles as built in build pipeline")

    query = """
    UPDATE raw_articles
    SET is_built = TRUE
    WHERE id = ANY(%s)
    """
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(query, (article_ids,))
        conn.commit()
        logger.info(f"Marked {len(article_ids)} articles as built")
    except Exception as e:
        logger.exception(
            f"Error marking articles with artcile id's {article_ids} as built: {e}"
        )
        raise
    finally:
        cursor.close()
        conn.close()


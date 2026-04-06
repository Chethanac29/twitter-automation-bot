from typing import List
from psycopg2.extras import execute_values

from app.db.connection import get_connection
from app.models.article import Article
from app.utils.logger import get_logger

logger = get_logger(__name__)

def insert_articles(articles: List[Article]) -> int:
    """
    Insert canonical articles into the database.
    Returns number of actual rows inserted.
    """

    if not articles:
        logger.info("No articles to insert.")
        return 0

    logger.info(f"Inserting {len(articles)} articles into the database...")

    insert_query = """
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
        VALUES %s
        ON CONFLICT (link) DO NOTHING
    """

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
        )
        for article in articles
    ]

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT COUNT(*) FROM articles;")
        before_count = cursor.fetchone()[0]

        execute_values(cursor, insert_query, values)
        conn.commit()

        cursor.execute("SELECT COUNT(*) FROM articles;")
        after_count = cursor.fetchone()[0]

        actual_inserted = after_count - before_count

        logger.info(
            f"Attempted to insert {len(articles)} canonical articles. "
            f"Actually inserted: {actual_inserted}"
        )

        return actual_inserted

    except Exception as e:
        conn.rollback()
        logger.exception(f"Error inserting canonical articles: {e}")
        raise

    finally:
        cursor.close()
        conn.close()


def fetch_unprocessed_articles(limit: int = 50) -> List[Article]:
    """
    Fetch unprocessed canonical articles from the database.
    """
    logger.info(f"Fetching up to {limit} unprocessed articles from the database...")

    query = """
        SELECT
            id,
            external_id,
            title,
            summary,
            content,
            link,
            source_domain,
            source_name,
            published_at,
            created_at,
            is_processed,
            processed_at
        FROM articles
        WHERE is_processed = FALSE
        ORDER BY published_at ASC
        LIMIT %s;
    """

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(query, (limit,))
        rows = cursor.fetchall()

        logger.info(f"Fetched {len(rows)} unprocessed articles from the database.")

        articles = []

        for row in rows:
            articles.append(
                Article(
                    id=row[0],
                    external_id=row[1],
                    title=row[2],
                    summary=row[3],
                    content=row[4],
                    link=row[5],
                    source_domain=row[6],
                    source_name=row[7],
                    published_at=row[8],
                    created_at=row[9],
                    is_processed=row[10],
                    processed_at=row[11]
                )
            )

        return articles

    except Exception as e:
        logger.exception(f"Error fetching unprocessed articles: {e}")
        raise

    finally:
        cursor.close()
        conn.close()


def mark_articles_as_processed(article_ids: List[int]):
    """
    Mark articles as processed from the given list of article ids.
    """

    if not article_ids:
        logger.info("No article ids provided to mark as processed.")
        return

    logger.info(f"Marking {len(article_ids)} articles as processed...")

    query = """
        UPDATE articles
        SET
            is_processed = TRUE,
            processed_at = NOW()
        WHERE id = ANY(%s)
    """

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(query, (article_ids,))
        conn.commit()
        logger.info(f"Marked {len(article_ids)} articles as processed.")

    except Exception as e:
        conn.rollback()
        logger.exception(f"Error marking article ids {article_ids} as processed: {e}")
        raise

    finally:
        cursor.close()
        conn.close()
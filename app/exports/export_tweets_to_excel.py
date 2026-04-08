import os
import pandas as pd

from app.db.connection import get_connection
from app.utils.logger import get_logger

logger = get_logger(__name__)


def fetch_tweets_for_export(status: str = "pending", limit: int = 100):
    """
    Fetch tweets from DB for export.
    """
    logger.info(f"Fetching up to {limit} tweets with status='{status}' for export...")

    query = """
        SELECT
            id,
            article_id,
            tweet_text,
            platform,
            status,
            created_at,
            posted_at
        FROM tweets
        WHERE status = %s
        ORDER BY created_at ASC
        LIMIT %s;
    """

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(query, (status, limit))
        rows = cursor.fetchall()
        logger.info(f"Fetched {len(rows)} tweets for export.")
        return rows

    except Exception as e:
        logger.exception(f"Error fetching tweets for export: {e}")
        raise

    finally:
        cursor.close()
        conn.close()


def export_tweets_to_excel(status: str = "pending", limit: int = 100):
    """
    Export tweets to Excel file.
    """
    rows = fetch_tweets_for_export(status=status, limit=limit)

    if not rows:
        logger.info("No tweets found for export.")
        print("No tweets found for export.")
        return

    columns = [
        "id",
        "article_id",
        "tweet_text",
        "platform",
        "status",
        "created_at",
        "posted_at"
    ]

    df = pd.DataFrame(rows, columns=columns)

    os.makedirs("exports", exist_ok=True)

    output_file = f"exports/tweets_export_{status}.xlsx"
    df.to_excel(output_file, index=False)

    logger.info(f"Exported {len(df)} tweets to {output_file}")
    print(f"Exported {len(df)} tweets to {output_file}")


if __name__ == "__main__":
    export_tweets_to_excel(status="pending", limit=100)
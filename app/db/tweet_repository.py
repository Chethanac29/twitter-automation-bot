from typing import List
from psycopg2.extras import execute_values

from app.db.connection import get_connection
from app.models.tweet import Tweet
from app.utils.logger import get_logger

logger = get_logger(__name__)

def insert_tweets(tweets: List[Tweet]) -> int:
    '''
    Insert the generated tweets into the database.
    Return the number of tweets inserted.
    '''
    if not tweets:
        logger.info('No tweets to insert.')
        return 0

    logger.info(f'Inserting {len(tweets)} into the database.')

    query = '''
    INSERT INTO tweets (
        article_id,
        tweet_text,
        platform,
        status
    ) VALUES %s
    '''
    values = [
        (
            tweet.article_id,
            tweet.tweet_text,
            tweet.platform,
            tweet.status
        ) for tweet in tweets
    ]

    conn = get_connection()
    cursor = conn.cursor()

    try:
        execute_values(cursor, query, values)
        conn.commit()

        logger.info(f'Inserted {len(tweets)} tweets into the database.')
        return len(tweets)
    except Exception as e:
        logger.error(f'Error inserting tweets: {e}')
        conn.rollback()
        return 0
    finally:
        cursor.close()
        conn.close()

def fetch_pending_tweets(limit: int = 100) -> List[Tweet]:
    '''
    Fetch the tweets that are pending to be posted.
    '''
    logger.info(f'Fetching up to {limit} pending tweets from the database.')

    query = '''
    SELECT id, article_id, tweet_text, platform, status
    FROM tweets
    WHERE status = 'pending'
    ORDER BY created_at ASC
    LIMIT %s
    '''

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(query, (limit,))
        rows = cursor.fetchall()

        tweets  = []

        for row in rows:
            tweets.append(
                Tweet(
                    id=row[0],
                    article_id=row[1],
                    tweet_text=row[2],
                    platform=row[3],
                    status=row[4],
                    created_at=row[5],
                    posted_at=row[6]
                )
            )
        logger.info(f'Fetched {len(tweets)} pending tweets from the database.')
        return tweets
    except Exception as e:
        logger.error(f'Error fetching pending tweets: {e}')
        return []
    finally:
        cursor.close()
        conn.close()

def mark_tweet_as_posted(tweet_id: int):
    """
    Mark a tweet as successfully posted.
    """
    logger.info(f"Marking tweet id={tweet_id} as posted...")

    query = """
        UPDATE tweets
        SET
            status = 'posted',
            posted_at = NOW()
        WHERE id = %s;
    """

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(query, (tweet_id,))
        conn.commit()
        logger.info(f"Tweet id={tweet_id} marked as posted.")

    except Exception as e:
        conn.rollback()
        logger.exception(f"Error marking tweet id={tweet_id} as posted: {e}")
        raise

    finally:
        cursor.close()
        conn.close()


def mark_tweet_as_failed(tweet_id: int):
    """
    Mark a tweet as failed to post.
    """
    logger.info(f"Marking tweet id={tweet_id} as failed...")

    query = """
        UPDATE tweets
        SET status = 'failed'
        WHERE id = %s;
    """

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(query, (tweet_id,))
        conn.commit()
        logger.info(f"Tweet id={tweet_id} marked as failed.")

    except Exception as e:
        conn.rollback()
        logger.exception(f"Error marking tweet id={tweet_id} as failed: {e}")
        raise

    finally:
        cursor.close()
        conn.close()

from app.db.tweet_repository import (
    fetch_pending_tweets,
    mark_tweet_as_posted,
    mark_tweet_as_failed,
)
from app.posting.threads_poster import post_to_threads
from app.utils.logger import get_logger

logger = get_logger(__name__)


def run_threads_posting_pipeline(limit: int = 50):
    """
    Fetch pending tweets and post them to Threads.
    """

    logger.info("Starting Threads posting pipeline...")

    tweets = fetch_pending_tweets(limit=limit)

    if not tweets:
        logger.info("No pending tweets found. Exiting pipeline.")
        return

    logger.info(f"Fetched {len(tweets)} pending tweets for Threads posting.")

    for tweet in tweets:
        try:
            success = post_to_threads(tweet)

            if success:
                mark_tweet_as_posted(tweet.id)
            else:
                mark_tweet_as_failed(tweet.id)

        except Exception as e:
            logger.exception(f"Unexpected error while posting tweet id={tweet.id}: {e}")
            mark_tweet_as_failed(tweet.id)

    logger.info("Threads posting pipeline completed.")


if __name__ == "__main__":
    run_threads_posting_pipeline()
from typing import List, Tuple

from app.models.article import Article
from app.models.tweet import Tweet

from app.db.article_repository import (
    fetch_unprocessed_articles,
    mark_articles_as_processed,
)
from app.db.tweet_repository import insert_tweets

from app.generation.tweet_generator import generate_tweet
from app.utils.logger import get_logger

logger = get_logger(__name__)


# =========================================
# VALIDATION / CLEANUP
# =========================================
def is_valid_tweet(tweet_text: str) -> bool:
    """
    Basic tweet quality validation.
    """

    if not tweet_text:
        return False

    if len(tweet_text.strip()) < 40:
        return False

    if len(tweet_text.strip()) > 500:  # safe-ish for Threads
        return False

    bad_prefixes = [
        "Tweet:",
        "**Tweet:**",
        "{",
        "[",
    ]

    if any(tweet_text.strip().startswith(prefix) for prefix in bad_prefixes):
        return False

    return True


# =========================================
# GENERATE TWEETS
# =========================================
def build_tweets(articles: List[Article], platform: str = "threads") -> Tuple[List[Tweet], List[int]]:
    """
    Generate tweets for articles.
    Returns:
        - list of valid Tweet objects
        - list of successfully processed article IDs
    """

    tweets = []
    successful_article_ids = []

    for article in articles:
        try:
            tweet = generate_tweet(article, platform=platform)

            if not is_valid_tweet(tweet.tweet_text):
                logger.warning(
                    f"Generated invalid tweet for article id={article.id}. Skipping."
                )
                continue

            tweets.append(tweet)
            successful_article_ids.append(article.id)

            logger.info(f"Tweet built for article id={article.id}")

        except Exception as e:
            logger.exception(
                f"Failed to generate tweet for article id={article.id}: {e}"
            )

    logger.info(f"Built {len(tweets)} valid tweets from {len(articles)} articles.")

    return tweets, successful_article_ids


# =========================================
# MAIN PIPELINE
# =========================================
def run_tweet_generation_pipeline(limit: int = 50, platform: str = "threads"):
    """
    Main tweet generation pipeline.
    """

    logger.info("Starting tweet generation pipeline...")

    # =========================================
    # STEP 1: Fetch unprocessed articles
    # =========================================
    articles = fetch_unprocessed_articles(limit=limit)

    if not articles:
        logger.info("No unprocessed articles found. Exiting pipeline.")
        return

    logger.info(f"Fetched {len(articles)} unprocessed articles.")

    # =========================================
    # STEP 2: Generate tweets
    # =========================================
    tweets, successful_article_ids = build_tweets(articles, platform=platform)

    if not tweets:
        logger.info("No valid tweets generated. Exiting pipeline.")
        return

    # =========================================
    # STEP 3: Insert tweets into DB
    # =========================================
    inserted_count = insert_tweets(tweets)
    logger.info(f"Inserted {inserted_count} tweets into the database.")

    # =========================================
    # STEP 4: Mark articles as processed
    # =========================================
    mark_articles_as_processed(successful_article_ids)

    logger.info("Tweet generation pipeline completed successfully.")


if __name__ == "__main__":
    run_tweet_generation_pipeline()
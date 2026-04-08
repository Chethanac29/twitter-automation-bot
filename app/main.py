import time
from app.ingestion.ingestion_pipeline import run_ingestion_pipeline
from app.posting.threads_posting_pipeline import run_threads_posting_pipeline
from app.processing.article_builder_pipeline import run_article_builder_pipeline
from app.utils.logger import get_logger
from app.generation.tweet_generation_pipeline import run_tweet_generation_pipeline

logger = get_logger(__name__)
def main():
    print("Hello from twitter-automation-bot!")
    while True:
        logger.info("Starting main loop of twitter-automation-bot...")

        # Step 1: Run the ingestion pipeline to fetch new tweets
        run_ingestion_pipeline()

        # Step 2: Run the article builder pipeline to create articles from tweets
        run_article_builder_pipeline()

        # Step 3: Run the tweet generation pipeline to create new tweets based on articles
        run_tweet_generation_pipeline()

        # Step 4: Run the Threads posting pipeline to post tweets to Threads
        run_threads_posting_pipeline()

        logger.info("Main loop completed. Sleeping for 1 minute before next iteration...")
        time.sleep(60)  # Sleep for 1 minute before running the loop again

    



if __name__ == "__main__":
    main()

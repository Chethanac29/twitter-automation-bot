import requests
from typing import Optional

from app.models.tweet import Tweet
from app.utils.logger import get_logger
from app.config.settings import THREADS_API_KEY

logger = get_logger(__name__)

GRAPH_API_BASE = "https://graph.threads.net/v1.0"


def create_threads_container(text_content: str) -> Optional[str]:
    url = f"{GRAPH_API_BASE}/me/threads"

    payload = {
        "media_type": "TEXT",
        "text": text_content,
        "access_token": THREADS_API_KEY,
    }

    try:
        response = requests.post(url, data=payload, timeout=30)

        if not response.ok:
            logger.error(f"Threads API Error: {response.text}")
            return None

        data = response.json()
        container_id = data.get("id")

        if not container_id:
            logger.error(f"No container_id returned: {data}")
            return None

        return container_id

    except Exception as e:
        logger.exception(f"Error creating Threads container: {e}")
        return None

def publish_threads_container(container_id: str) -> bool:
    """
    Step 2: Publish Threads container.
    Returns True if successful.
    """

    url = f"{GRAPH_API_BASE}/me/threads_publish"

    payload = {
        "creation_id": container_id,
        "access_token": THREADS_API_KEY,
    }

    try:
        response = requests.post(url, data=payload, timeout=30)

        if not response.ok:
            logger.error(f"Threads Publish API Error: {response.text}")
            return False

        data = response.json()
        logger.info(f"Threads post published successfully: {data}")
        return True

    except Exception as e:
        logger.exception(f"Error publishing Threads container: {e}")
        return False


def post_to_threads(tweet: Tweet) -> bool:
    """
    Post a Tweet object to Threads.
    Returns True if posting succeeds, False otherwise.
    """

    logger.info(f"Attempting to post tweet id={tweet.id} to Threads...")

    if not tweet.tweet_text or not tweet.tweet_text.strip():
        logger.error(f"Tweet id={tweet.id} has empty tweet_text. Cannot post.")
        return False

    container_id = create_threads_container(tweet.tweet_text)

    if not container_id:
        logger.error(f"Failed to create Threads container for tweet id={tweet.id}")
        return False

    success = publish_threads_container(container_id)

    if success:
        logger.info(f"Tweet id={tweet.id} posted successfully to Threads.")
    else:
        logger.error(f"Tweet id={tweet.id} failed to publish to Threads.")

    return success
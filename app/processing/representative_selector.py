from typing import List
from datetime import datetime, timezone

from app.models.article import Article
from app.utils.logger import get_logger

logger = get_logger(__name__)


from datetime import datetime


def compute_article_score(article: Article) -> float:
    """
    Compute a representative score based on:
    - content richness
    - recency
    - preference for fully scraped articles over weak fallback ones
    """

    title_len = len(article.title.strip()) if article.title else 0
    summary_len = len(article.summary.strip()) if article.summary else 0
    content_len = len(article.content.strip()) if article.content else 0

    # base richness
    richness_score = (title_len * 0.5) + (summary_len * 1.0) + (content_len * 1.5)

    # bonus for richer article body
    full_content_bonus = 200 if content_len >= 500 else 0

    # recency bonus
    recency_bonus = 0
    if article.published_at:
        try:
            now = datetime.utcnow()
            age_hours = (now - article.published_at).total_seconds() / 3600
            recency_bonus = max(0, 72 - age_hours)  # newer gets small bonus
        except Exception:
            recency_bonus = 0

    return richness_score + full_content_bonus + recency_bonus


def select_representative_article(cluster: List[Article]) -> Article:
    """
    Select the best representative article from the cluster.
    """

    if not cluster:
        logger.warning("Empty cluster provided for representative selection.")
        raise ValueError("Cluster cannot be empty for representative selection.")

    best_article = max(cluster, key=compute_article_score)
    logger.info(
        f"Selected article: title='{best_article.title}', link='{best_article.link}' "
        f"from cluster size {len(cluster)}"
    )
    return best_article


def select_representative_articles(clusters: List[List[Article]]) -> List[Article]:
    """
    Select one representative article from each cluster.
    """

    if not clusters:
        logger.info("No clusters provided for representative selection.")
        return []

    representatives = [select_representative_article(cluster) for cluster in clusters]

    logger.info(f"Selected {len(representatives)} representative articles.")

    return representatives

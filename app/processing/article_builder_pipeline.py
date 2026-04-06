from typing import List, Tuple

from app.models.article import Article
from app.models.raw_article import RawArticle

from app.db.raw_articles_repository import (
    fetch_unbuilt_raw_articles,
    mark_articles_as_built
)

from app.db.article_repository import insert_articles

from app.processing.scraper import scrape_artcile_content
from app.processing.article_transformer import build_article
from app.processing.embedder import generate_embeddings
from app.processing.clusterer import cluster_articles, compute_similarity_matrix
from app.processing.representative_selector import select_representative_articles

from app.utils.logger import get_logger

logger = get_logger(__name__)


def build_article_candidates(raw_articles: List[RawArticle]) -> Tuple[List[Article], List[int]]:
    """Build article candidates from the raw articles"""
    article_candidates = []
    successful_raw_ids = []

    for raw_article in raw_articles:
        try:
            content = scrape_artcile_content(raw_article)
            article = build_article(raw_article, content)
            article_candidates.append(article)
            successful_raw_ids.append(raw_article.id)
        except Exception as e:
            logger.error(f"Failed to build article from raw article {raw_article.id}: {e}")

    logger.info(f"Built {len(article_candidates)} article candidates from {len(raw_articles)} raw articles.")
    return article_candidates, successful_raw_ids


def run_article_builder_pipeline(limit: int = 100):
    """main article builder pipeline"""
    logger.info("Starting the article builder pipeline...")

    # fetch raw articles
    raw_articles = fetch_unbuilt_raw_articles(limit=limit)

    if not raw_articles:
        logger.info("No unbuilt raw articles found. Exiting pipeline.")
        return

    logger.info(f"Fetched {len(raw_articles)} unbuilt raw articles.")

    # build article candidates
    article_candidates, successful_raw_ids = build_article_candidates(raw_articles)

    if not article_candidates:
        logger.info("No article candidates built. Exiting pipeline.")
        return

    logger.info(f"Built {len(article_candidates)} article candidates. Generating embeddings...")

    # generate embeddings
    embeddings = generate_embeddings(article_candidates)
    if len(embeddings) == 0:
        logger.info("No embeddings generated. Exiting pipeline.")
        return

    logger.info(f"Generated {len(embeddings)} embeddings.")

    # clustering
    similarity_matrix = compute_similarity_matrix(embeddings)
    clusters = cluster_articles(
        articles=article_candidates,
        similarity_matrix=similarity_matrix
    )

    if not clusters:
        logger.info("No clusters formed. Exiting pipeline.")
        return

    logger.info(f"Created {len(clusters)} clusters.")
    for idx, cluster in enumerate(clusters, start=1):
        logger.info(f"Cluster {idx}: {len(cluster)} articles")

    # representative selection
    representative_articles = select_representative_articles(clusters)

    if not representative_articles:
        logger.info("No representative articles selected. Exiting pipeline.")
        return

    logger.info(f"Selected {len(representative_articles)} representative articles. Inserting into database...")

    logger.info("Representative article titles:")
    for article in representative_articles:
        logger.info(f"- {article.title}")

    # insert into DB
    inserted_count = insert_articles(representative_articles)
    logger.info(f"Inserted {inserted_count} representative articles into the database.")

    # mark raw articles as built
    mark_articles_as_built(successful_raw_ids)

    logger.info("Article builder pipeline completed successfully.")


if __name__ == "__main__":
    run_article_builder_pipeline()
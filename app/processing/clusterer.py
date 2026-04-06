from typing import List
from sklearn.metrics.pairwise import cosine_similarity

from app.models.article import Article
from app.utils.logger import get_logger

logger = get_logger(__name__)

SIMILARITY_THRESHOLD = 0.85


def compute_similarity_matrix(embeddings):
    """
    Compute similarity matrix from embeddings using cosine similarity.
    """
    return cosine_similarity(embeddings)


def cluster_articles(
    articles: List[Article],
    similarity_matrix,
    threshold: float = SIMILARITY_THRESHOLD
) -> List[List[Article]]:
    """
    Cluster articles using graph-based connected components.
    """

    if not articles:
        logger.info("No articles provided for clustering.")
        return []

    logger.info(
        f"Clustering {len(articles)} articles with similarity threshold: {threshold}..."
    )

    visited = set()
    clusters = []

    for i in range(len(articles)):
        if i in visited:
            continue

        # BFS / DFS stack
        stack = [i]
        cluster_indices = []

        while stack:
            node = stack.pop()

            if node in visited:
                continue

            visited.add(node)
            cluster_indices.append(node)

            # find neighbors
            for j in range(len(articles)):
                if j not in visited and similarity_matrix[node][j] >= threshold:
                    stack.append(j)

        cluster = [articles[idx] for idx in cluster_indices]
        clusters.append(cluster)

    logger.info(
        f"Clustering completed. Formed {len(clusters)} clusters from {len(articles)} articles."
    )

    return clusters
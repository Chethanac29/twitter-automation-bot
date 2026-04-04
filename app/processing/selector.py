from datetime import datetime
from typing import List

def normalize(values):
    min_v = min(values)
    max_v = max(values)

    if min_v == max_v:
        return [1.0 for _ in values]

    return [(v - min_v) / (max_v - min_v) for v in values]

def select_representative(cluster):

    content_length = [len(article.content or "") for article in cluster]
    summary_length = [len(article.summary or "") for article in cluster]

    timestamps = [article.published_at.timestamp() if article.published_at else 0 for article in cluster]

    #Normalize
    content_scorees = normalize(content_length)
    summary_scores = normalize(summary_length)
    recency_scores = normalize(timestamps)

    final_scores = []

    for i in range(len(cluster)):
        score = (
            0.5 * content_scorees[i] + #informative content
            0.3 * summary_scores[i] +
            0.2 * recency_scores[i] #recency
        )
        final_scores.append(score)
    best_index = final_scores.index(max(final_scores))

    return cluster[best_index]

def select_from_cluster(clusters):
    representatives = []

    for cluster in clusters:
        best = select_representative(cluster)
        representatives.append(best)

    return representatives
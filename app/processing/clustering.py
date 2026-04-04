from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


model = SentenceTransformer('all-MiniLM-L6-v2')

SIMILARITY_THRESHOLD = 0.65
def prepare_text(article):
    text = (article.title + ' ' + article.summary).lower()

    #need to remove the noise words from the test
    noise_words = ['cricket', 'ipl', 'match', 't20', 'world cup', 'odi', 'test', 'series', 'league',"ipl 2026","season","team", "2026"]
    for word in noise_words:
        text = text.replace(word, '')
    
    return text.strip()

def generate_embeddings(articles):
    texts = [prepare_text(article) for article in articles]
    embeddings = model.encode(texts,show_progress_bar=True)

    return embeddings

def compute_similarity_matrix(embeddings):
    return cosine_similarity(embeddings)

def cluster_articles(articles, similarity_matrix, threshold=SIMILARITY_THRESHOLD):
    clusters = []
    visited = set()

    print('Similarity score sample:', similarity_matrix[0][:10])

    for i in range(len(articles)):
        if i in visited:
            continue

        cluster = []
        queue = [i]
        visited.add(i)

        while queue:
            current = queue.pop()
            cluster.append(current)

            for j in range(len(articles)):
                if j not in visited and similarity_matrix[current][j] > threshold:
                    visited.add(j)
                    queue.append(j)

        clusters.append(cluster)

    return clusters

def build_clustered_articles(articles,clusters):
    clustered = []
    for cluster in clusters:
        grouped = [articles[i] for i in cluster]
        clustered.append(grouped)
    
    return clustered

def cluster_pipeline(articles):
    embeddings = generate_embeddings(articles)
    sim_matrix = compute_similarity_matrix(embeddings)
    
    clusters = cluster_articles(articles,sim_matrix)

    return build_clustered_articles(articles,clusters)

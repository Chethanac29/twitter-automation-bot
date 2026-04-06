from typing import List
from sentence_transformers import SentenceTransformer

from app.models.article import Article
from app.utils.logger import get_logger


logger = get_logger(__name__)

model = SentenceTransformer('all-MiniLM-L6-v2')

def prepare_text(article: Article) -> str:
    '''
    Preapre the text for embedding.
    Uses title + summary + first 1000 characters of the content.
    '''

    content_snippet = article.content[:1000] if article.content else ""

    return f'''
        Title: {article.title}

        Summary: {article.summary}

        Content: {content_snippet}
    '''.strip()

def generate_embeddings(articles: List[Article]):
    '''Generate embeddings for the given list of articles objects'''
    if not articles:
        logger.info('No articles provided to generate embeddings.')
        return []
    
    logger.info(f'Generating embeddings for {len(articles)} articles...')

    texts = [prepare_text(article) for article in articles]
    embeddings = model.encode(texts, show_progress_bar=True)

    logger.info('Embedding generation completed.')

    return embeddings
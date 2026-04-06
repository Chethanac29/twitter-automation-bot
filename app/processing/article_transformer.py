# from datetime import datetime, timezone
# from models.raw_article import RawArticle
# from models.article import Article

# SOURCE_MAPPING = {
#     "www.espncricinfo.com": "ESPN Cricinfo",
#     "sportstar.thehindu.com": "The Hindu Sportstar"
# }

# def build_article(raw_article: RawArticle, content: str) -> Article:
#     source_domain = raw_article.source
#     source_name = SOURCE_MAPPING.get(source_domain,source_domain)

#     return Article(
#         external_id = raw_article.external_id,
#         title = raw_article.title,
#         summary = raw_article.summary,
#         content = content,
#         link = raw_article.link,
#         source_domain = source_domain,
#         source_name = source_name,
#         published_at = raw_article.published_at,
#         created_at = datetime.now(timezone.utc)
#     )
from urllib.parse import urlparse

from app.models.raw_article import RawArticle
from app.models.article import Article
from app.utils.logger import get_logger

logger = get_logger(__name__)

def extract_source_domain(link: str) -> str:
    '''
    Extract the source domain from the article link
    '''
    parsed_url = urlparse(link)
    return parsed_url.netloc

def build_article(raw_article: RawArticle, content:str) -> Article:
    '''Transform the raw article + scraped content into Article object'''
    source_domain = extract_source_domain(raw_article.link)
    logger.info(f"Building article → title: {raw_article.title}")
    return Article(
        external_id=raw_article.external_id,
        title=raw_article.title,
        summary=raw_article.summary,
        content=content,
        link=raw_article.link,
        source_domain=source_domain,
        source_name=raw_article.source,
        published_at=raw_article.published_at
    )

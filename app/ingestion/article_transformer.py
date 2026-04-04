from datetime import datetime, timezone
from models.raw_article import RawArticle
from models.article import Article

SOURCE_MAPPING = {
    "www.espncricinfo.com": "ESPN Cricinfo",
    "sportstar.thehindu.com": "The Hindu Sportstar"
}

def build_article(raw_article: RawArticle, content: str) -> Article:
    source_domain = raw_article.source
    source_name = SOURCE_MAPPING.get(source_domain,source_domain)

    return Article(
        external_id = raw_article.external_id,
        title = raw_article.title,
        summary = raw_article.summary,
        content = content,
        link = raw_article.link,
        source_domain = source_domain,
        source_name = source_name,
        published_at = raw_article.published_at,
        created_at = datetime.now(timezone.utc)
    )
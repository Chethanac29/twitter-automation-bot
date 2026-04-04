import psycopg2
from psycopg2.extras import execute_values
from typing import List

from models.raw_article import RawArticle


def insert_raw_articles(conn, raw_articles: List[RawArticle]):
    if not raw_articles:
        return
    
    query = """
            INSERT INTO raw_articles (
            external_id,
            title,
            summary,
            link,
            published_at,
            source
            ) VALUES %s
            ON CONFLICT (external_id, source) DO NOTHING
            """
    values = [
        (
            article.external_id,
            article.title,
            article.summary,
            article.link,
            article.published_at,
            article.source
        ) for article in raw_articles
    ]
    with conn.cursor() as cursor:
        execute_values(cursor, query, values)
    
    conn.commit()

from typing import List
import time

from models.article import Article
from models.raw_article import RawArticle

from app.build.scraper import scrape_article
from ingestion.rss_fetcher import fetch_rss_articles
from app.build.article_transformer import build_article

from db.connection import get_connection
from db.raw_articles_repository import insert_raw_articles



TIME_DELAY = 1
BLOCKED_SOURCES = {
    "www.espncricinfo.com"
}

def ingest_pipeline(rss_feeds: List[str]) -> List[Article]:
    # Step 1 : fetching the raw articles 
    raw_articles = fetch_rss_articles(rss_feeds)

    #step 2 : store the raw-articles to raw articles table
    conn = get_connection()
    insert_raw_articles(conn=conn, raw_articles=raw_articles)


    
    articles = []
    for raw_article in raw_articles:
        if raw_article.source in BLOCKED_SOURCES:
            content = raw_article.summary
        else:
            scraped_content = scrape_article(raw_article.link)
            content = scraped_content or raw_article.summary

        article = build_article(raw_article, content)

        time.sleep(TIME_DELAY) # to avoid hitting the server too fast
        articles.append(article)
        
    return articles

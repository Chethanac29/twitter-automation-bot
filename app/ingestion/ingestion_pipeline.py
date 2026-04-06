from app.ingestion.raw_article_loader import load_raw_articles
from app.utils.logger import get_logger

logger = get_logger(__name__)
RSS_FEEDS = [
    "https://sportstar.thehindu.com/cricket/ipl/feeder/default.rss",
    "https://www.espncricinfo.com/rss/content/story/feeds/0.xml",
    "https://sports.ndtv.com/rss/cricket",
    "https://timesofindia.indiatimes.com/rssfeeds/54829575.cms",
    "https://www.hindustantimes.com/feeds/rss/cricket/ipl/rssfeed.xml",
    "https://www.cricbuzz.com/rss/content/story/feeds/0.xml",
    "https://www.indiatvnews.com/rssnews/topstory-sports.xml",
    "https://cricketmood.com/rss.xml",
]

def run_ingestion_pipeline():
    '''Run the ingestion pipeline to fetch and store raw articles.'''
    logger.info('=='*5 + ' Starting the ingestion pipeline... ' + '=='*5)
    count = load_raw_articles(RSS_FEEDS)
    logger.info('=='*5 + f' Ingestion pipeline completed. {count} articles processed. ' + '=='*5)


if __name__ == "__main__":
    
    run_ingestion_pipeline()
    
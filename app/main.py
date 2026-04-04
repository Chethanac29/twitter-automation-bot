import time
from ingestion.piepeline import ingest_pipeline
from processing.clustering import cluster_pipeline
from processing.selector import select_from_cluster
from llm.tweet_generator import generate_tweet
from posting.post_tweet import post_to_threads
BLOCKED_SOURCES = {
    "www.espncricinfo.com"
} 


def main():
    print("Hello from twitter-automation-bot!")
    rss_feeds = ["https://sportstar.thehindu.com/cricket/ipl/feeder/default.rss",
                 "https://www.espncricinfo.com/rss/content/story/feeds/0.xml"]
    
    articles = ingest_pipeline(rss_feeds)

    # print(f"Total number of articles processed {len(articles)}")
    # for article in articles:
        
    #     print("-" * 50)
    #     print("Title: ", article.title)
    #     print("source: ", article.source_name)
    #     print("Content Preview: ", article.content[:100])
    
    clusters = cluster_pipeline(articles)
    # print('Total cluster articles: ', len(clusters))

    # for i, cluster in enumerate(clusters[:5]):
    #     print(f"\nCluster {i+1}:")
    #     for article in cluster:
    #         print("-", article.title)
    
    representatives = select_from_cluster(clusters)
    
    # print(f"Selected {len(representatives)} representative articles")

    for article in representatives:
        tweet_json = generate_tweet(article)

        print("\n" + "="*50)
        print(tweet_json)
        if tweet_json == "" or len(tweet_json) < 50:
            continue 
        else:
            post_to_threads(text_content=tweet_json)
        



if __name__ == "__main__":
    main()

from newspaper import Article
from typing import Optional


def scrape_article(link : str) -> Optional[str]:
    try:
        article = Article(link)
        article.config.browser_user_agent = (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        )
        article.download()
        article.parse()

        content = article.text

        if not content or len(content.strip()) < 10:
            print(f"Warning: No content found for {link}")
            return None
        return content
    except Exception as e:
        print(f"Error scraping {link}: {e}")
        return None
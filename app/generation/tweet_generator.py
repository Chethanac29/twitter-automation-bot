from pydantic import BaseModel, Field
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

from app.models.article import Article
from app.models.tweet import Tweet
from app.generation.prompt_template import get_prompt
from app.utils.logger import get_logger

from dotenv import load_dotenv
import os

load_dotenv()
OPEN_ROUTER_API_KEY = os.getenv("OPEN_ROUTER_API_KEY")
logger = get_logger(__name__)
GEMMA4 = os.getenv("GEMMA4")

# =========================================
# STRUCTURED OUTPUT SCHEMA
# =========================================
class TweetOutput(BaseModel):
    tweet_text: str = Field(
        description="Final tweet text including hashtags. No labels, no markdown, no extra formatting."
    )


# =========================================
# LLM SETUP
# =========================================

# llm = ChatOpenAI(
#     model="google/gemma-4-31b-it",
#     temperature=0.7,
#     base_url="https://integrate.api.nvidia.com/v1/",
#     api_key=GEMMA4,
# )
llm = ChatOpenAI(
    model="qwen/qwen3.6-plus:free",
    temperature=0.7,
    base_url="https://openrouter.ai/api/v1",
    api_key=OPEN_ROUTER_API_KEY,
)
# llm = ChatOpenAI(
#     model="qwen3.5:9b",
#     temperature=0.7,
#     base_url="http://localhost:11434/v1",
#     api_key='ollama',
# )
structured_llm = llm.with_structured_output(TweetOutput)


# =========================================
# PROMPT SETUP
# =========================================
tweet_prompt = get_prompt()

tweet_prompt_template = PromptTemplate(input_variables=["news"], template=tweet_prompt)

chain = tweet_prompt_template | structured_llm


# =========================================
# HELPERS
# =========================================
def build_news_input(article: Article) -> str:
    """
    Build formatted news context for tweet generation.
    """

    content_snippet = article.content[:3000] if article.content else ""

    return f"""
        Title: {article.title}

        Summary: {article.summary}

        Content:
        {content_snippet}
        """.strip()


# =========================================
# MAIN GENERATOR
# =========================================
def generate_tweet(article: Article, platform: str = "threads") -> Tweet:
    """
    Generate a tweet for a given article and return a Tweet object.
    """

    logger.info(f"Generating tweet for article id={article.id} | title={article.title}")

    news = build_news_input(article)

    response: TweetOutput = chain.invoke({"news": news})

    tweet_text = response.tweet_text.strip()

    logger.info(f"Tweet generated successfully for article id={article.id}")

    return Tweet(
        article_id=article.id,
        tweet_text=tweet_text,
        platform=platform,
        status="pending",
    )


if __name__ == "__main__":
    # Example usage
    sample_article = Article(
        id=1,
        title="TATA IPL 2026, Match 11: RCB vs CSK – Match Report",
        summary="The M. Chinnaswamy Stadium witnessed a high-octane encounter as Royal Challengers Bengaluru (RCB) registered an emphatic 43-run victory over the Chennai Super Kings (CSK) in Match 11 of TATA IPL 2026. In a match defined by relentless power-hitting, RCB posted a colossal 250/3, the highest-ever total recorded against CSK in IPL history, before restricting the visitors to 207.",
        content="""
        The M. Chinnaswamy Stadium witnessed a high-octane encounter as Royal Challengers Bengaluru (RCB) registered an emphatic 43-run victory over the Chennai Super Kings (CSK) in Match 11 of TATA IPL 2026. In a match defined by relentless power-hitting, RCB posted a colossal 250/3, the highest-ever total recorded against CSK in IPL history, before restricting the visitors to 207.Chennai Super Kings won the toss and opted to bowl, a decision that initially seemed balanced after Anshul Kamboj dismissed Virat Kohli (28 off 18) in the fifth over. However, the momentum shifted rapidly. Phil Salt (46 off 30) and Devdutt Padikkal (50 off 29) laid a solid foundation, but the true carnage began with the arrival of Tim David.


        David produced a finishing masterclass, remaining unbeaten on 70 off just 25 deliveriesat a staggering strike rate of 280.00. The highlight of the innings came in the 19th over, where David dismantled Jamie Overton for 30 runs (Sequence: 6, 2, 6, 6, 6, 4). One of these sixes, a monstrous 106-metre pull, sailed over the stadium roof, leaving the Bengaluru crowd in awe. Rajat Patidar provided the perfect foil at the other end, smashing an unbeaten 48 off 19 balls*. Together, the duo added an unbeaten 99-run partnership, propelling RCB to a daunting total of 250.


        Chasing 251, CSK required a flyer but faced immediate setbacks. Jacob Duffy struck in the first over to remove Ruturaj Gaikwad (7), followed quickly by the dismissal of Ayush Mhatre (1). Sarfaraz Khan kept the visitors in the hunt with a spirited 50 off 25 balls, but the mounting required run rate forced risky strokes as he was stumped in the bowling of Krunal Pandya.The RCB bowling unit remained disciplined throughout. Bhuvneshwar Kumar led the attack with precision, finishing with figures of 3/41 which also included a monumental feat as he became the second bowler in TATA IPL to complete 200 wickets. Suyash Sharma choked the middle overs, conceding only 21 runs in his four overs while picking up a wicket. Despite late-order resistance from Jamie Overton (37) and Prashant Veer (43), the target proved insurmountable. CSK were eventually bowled out for 207 in 19.4 overs handing RCB a famous victory. Tim David was adjudged the Player of the Match for his blistering knock that guided RCB to their second consecutive victory in their title defence.

        """,
    )

    generated_tweet = generate_tweet(sample_article)
    print(generated_tweet)

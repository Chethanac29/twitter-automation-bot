from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from models.tweet import Tweet
from models.article import Article
from typing import List, Optional


from llm.prompt_template import get_prompt, get_summary_prompt


from dotenv import load_dotenv

load_dotenv()


def build_news_input(article: Article):
    return f"""
    Title: {article.title}

    Summary: {article.summary}

    Content: 
    {article.content}
    """


def generate_tweet(article):
    news = build_news_input(article)

    response = chain.invoke({"news": news})
    return response.content


llm = ChatOpenAI(
    model="deepseek-r1:8b",
    temperature=0.7,
    base_url="http://localhost:11434/v1",
    api_key="ollama",
)
summariser_prompt = get_summary_prompt()

sum_prompt_template = PromptTemplate(
    input_variables=["news_content"], template=summariser_prompt
)

summary_template = get_prompt()

tweet_prompt_template = PromptTemplate(
    input_variables=["news"], template=summary_template
)
chain = tweet_prompt_template | llm

from crewai import Agent
from models import get_llm
from tools import NewsAPITool

def create_agents(model_name):
    llm = get_llm(model_name)
    
    news_fetcher = Agent(
        role='News Fetcher',
        goal='Fetch the latest news from BBC and The Verge.',
        backstory="You are responsible for gathering news from trusted sources.",
        verbose=True,
        llm=llm,
        tools=[NewsAPITool()],
        memory=True
    )

    news_summarizer = Agent(
        role='News Summarizer',
        goal='Summarize and organize the news fetched by the News Fetcher.',
        backstory="You excel at extracting key insights and summarizing news into a structured format.",
        verbose=True,
        llm=llm,
        allow_delegation=False,
        memory=True
    )

    return news_fetcher, news_summarizer
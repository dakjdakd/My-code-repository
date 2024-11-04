from crewai_tools import BaseTool
from newsapi import NewsApiClient

class NewsAPITool(BaseTool):
    name: str = "News API Tool"
    description: str = "Fetches top news headlines from specified sources using the NewsAPI."

    def _run(self, argument: str) -> str:
        newsapi = NewsApiClient(api_key='d9ffad634dcb46a3837d9d412e6d8d66')
        top_headlines = newsapi.get_top_headlines(
            sources='bbc-news,the-verge',
            language='en'
        )
        news_report = ""
        for i, article in enumerate(top_headlines['articles'], start=1):
            news_report += f"--------------------- Article{i} ---------------------\n"
            news_report += f"    Title: {article['title']}\n"
            news_report += f"    Description: {article['description']}\n"
            news_report += f"    URL: {article['url']}\n"
        return news_report

def cache_news(args, result):
    return result.count("Article") > 5

NewsAPITool.cache_function = cache_news
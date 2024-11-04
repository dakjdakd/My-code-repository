from crewai import Task

class AppendTask(Task):
    def _save_output(self, output: str):
        if self.output_file:
            with open(self.output_file, "a", encoding="utf-8") as file:
                file.write(output)
                file.write("\n")

def create_tasks(news_fetcher, news_summarizer, output_markdown_file):
    fetch_news_task = AppendTask(
        description="""\
        Your task is to fetch the latest news from BBC and The Verge.
        Use the News API Tool to get the top headlines.
        After fetching the news, compile a detailed report with titles, descriptions, and URLs of the articles.
        """,
        expected_output="""\
        A detailed news report containing:
        1. Titles of the latest news articles from BBC and The Verge
        2. Brief descriptions of each article
        3. URLs for each article
        The report should be well-formatted and easy to read, following the specified format.
        """,
        agent=news_fetcher,
        async_execution=False,
        memory=True,
    )

    summarize_news_task = AppendTask(
        description="""\
        Your task is to summarize the news report provided by the News Fetcher.
        To get the news report, use the 'Ask question to coworker' tool to ask the News Fetcher for the latest news.
        Once you have the report, create a concise summary organized by source and topic, highlighting key insights.
        Your summary should be easy to read and understand, capturing the most important information from the original report.
        """,
        expected_output="""\
        A concise summary of the news report, including:
        1. Key headlines organized by source (BBC and The Verge).
        2. Main topics covered in the news.
        3. Brief highlights of the most important stories.
        4. Any notable trends or patterns in the news.
        5. Be especially careful not to miss a link !.
        The summary should be well-structured and provide a quick overview of the day's top news.
        Finally, output in markdown format.
        """,
        agent=news_summarizer,
        inputs={'news_report': fetch_news_task.output},
        output_file=output_markdown_file,
        memory=True,
    )

    return fetch_news_task, summarize_news_task
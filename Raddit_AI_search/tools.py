import praw
import time
from langchain.tools import tool

import time
import praw

class BrowserTool:
    @tool("Scrape reddit content")
    def scrape_reddit(max_comments_per_post=10):
        """Scrape Reddit content.
        
        Action: Scrape reddit content
        Action Input: {"max_comments_per_post": 10}
        """
        reddit = praw.Reddit(
            client_id="O7WtTiXeYFr3REydN2zuoA",
            client_secret="RfoQXG1SNvSMOpTt7bVraJkC2Y1Avw",
            user_agent="MyRedditApp/1.0 (by /u/Constant_Battle_8050)"
        )
        subreddit = reddit.subreddit("LocalLLaMA")
        scraped_data = []

        for post in subreddit.hot(limit=15):
            post_data = {"title": post.title, "url": post.url, "comments": []}

            try:
                post.comments.replace_more(limit=0)  # Load top-level comments only
                comments = post.comments.list()
                comments = list(comments)
                comments = comments[:max_comments_per_post]

                for comment in comments:
                    post_data["comments"].append(comment.body)

                scraped_data.append(post_data)

            except praw.exceptions.APIException as e:
                print(f"API Exception: {e}")
                time.sleep(60)  # Sleep for 1 minute before retrying

        # Format output
        formatted_output = ""
        for i, post in enumerate(scraped_data, start=1):
            formatted_output += f"\nPost {i}\n"
            formatted_output += "=" * 50 + "\n"
            formatted_output += f"Title: {post['title']}\n"
            formatted_output += f"URL: <<{post['url']}>>\n"  # Add markers around the URL
            formatted_output += "-" * 50 + "\n"
            formatted_output += "Comments:\n"
            for comment in post['comments']:
                formatted_output += f"  - {comment}\n"
                formatted_output += "-" * 20 + "\n"  # Separator between comments
            formatted_output += "=" * 50 + "\n"

        return formatted_output

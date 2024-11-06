from crewai import Task
from agents import explorer, writer, critic

class AppendTask(Task):
    def _save_output(self, output: str):
        """Override to append to the output file instead of overwriting."""
        if self.output_file:
            with open(self.output_file, "a", encoding="utf-8") as file:
                file.write(output)
                file.write("\n")

def create_tasks(output_markdown_file):
    task_report = AppendTask(
        description="""
        1. Use and summarize scraped data from the subreddit LocalLLama to make a detailed report on the latest rising projects in AI. 
        2. Use ONLY scraped data from LocalLLama to generate the report. 
        3. Your final answer MUST be a full analysis report, text only, ignoring any code or anything that isn't text. 
        4. The report has to have bullet points with 10-15 exciting new AI projects and tools and links. 
        5. Write names of every tool and project and links.
        6. Each bullet point MUST contain 6 sentences that refer to one specific AI company, product, model, or anything you found on the subreddit LocalLLama.
        7. There must be a link to the project on Reddit,And other links mentioned in the project.
        8. Ensure you capture every link from each Reddit item.
        """,
        agent=explorer,
        expected_output="A detailed report with bullet points containing 10-15 exciting new AI projects and tools. Each bullet point contains 6 sentences(At least 200 words!!).",
        output_file=output_markdown_file,
        timeout=6000
    )

    task_blog = AppendTask(
        description="""
        1. Write a blog post with text only, featuring a short but impactful headline and at least 10 paragraphs. 
        2. Begin with an exceptionally witty and humorous introduction (5-6 sentences) to grab the reader's attention. 
        3. Use emojis creatively in the introduction, conclusion, and for each project description to add fun and visual appeal. 
        4. The blog should summarize the report on the latest AI tools found on the LocalLLama subreddit. 
        5. The style and tone should be compelling, concise, fun, technical yet using layman terms for the general public. 
        6. Point out specific new, exciting projects, apps, and companies in the AI world. 
        7. Don't write "**Paragraph [number]:**", instead start new paragraphs on a new line. 
        8. Write names of projects and tools in BOLD. 
        9. ALWAYS include links to projects/tools/research papers. 
        10. ONLY include information from LocalLLAma. 
        11. End with a vivid, memorable, and hilariously entertaining summary (5-6 sentences) that encapsulates the excitement of the AI advancements discussed.
        12. If there are multiple related links, you can write multiple links.
        13. Note that the links correspond to different platforms. For example, Reddit, Github, Huggingfacce, and so on.
        
        Use the following markdown format for your output:
        ```
        ## [Witty Title] �

        [Exceptionally humorous introduction with creative emoji use]

        ## 1. [Post Title] 🚀
        If there is no corresponding link, you can not fill in
        - Reddit:(https://www.reddit.com/r/LocalLLaMA/comments/example.com)
        - Github:(https://github.com/example.com)
        - Page:(https://papeg.ai/example2.com)
        - Huggingface(https://huggingface.ai/example3.com)....
        ....(More other links)
        - facts(To describe in detail)
        - Personal thoughts on how it connects to the overall theme of the newsletter
        - Description of how the project disrupted the industry
        - Help for users
        
        (If there are multiple related links, you can write multiple links.)
        (If there is no corresponding link, you can not fill in)
        ## 2. [Post Title] 🧠
        - Reddit:(https://www.reddit.com/r/LocalLLaMA/comments/example.com)
        - Github:(https://github.com/example.com)
        - Page:(https://papeg.ai/example2.com)
        - Huggingface(https://huggingface.ai/example3.com)....
        ....(More other links)
        - facts(To describe in detail)
        - Personal thoughts on how it connects to the overall theme of the newsletter
        - Description of how the project disrupted the industry
        - Help for users
        
        (If there are multiple related links, you can write multiple links.)
        (If there is no corresponding link, you can not fill in)
        ## 3. [Post Title] 🚀
        - Reddit:(https://www.reddit.com/r/LocalLLaMA/comments/example.com)
        - Github:(https://github.com/example.com)
        - Page:((https://papeg.ai/example2.com)
        - Huggingface(https://huggingface.ai/example3.com)....
        ....(More other links)
        - facts(To describe in detail)
        - Personal thoughts on how it connects to the overall theme of the newsletter
        - Description of how the project disrupted the industry
        - Help for users
        ......

        ```
        [Vivid, memorable, and hilariously entertaining summary with creative emoji use]
        
        Remember to make the introduction and conclusion exceptionally witty, vivid, and entertaining. 
        Use emojis creatively to enhance the fun factor of your writing. 
        Here are some emoji examples for inspiration, but feel free to use others that fit the context better: 
        🌟, 🎉, 🍀, 🧠, 🦄, 🕶️, 🌈, 🔥, 🎨, 📚, 🎶, 🌍, 🚴‍♂️, 🐉, ✈️. 
        The key is to make the content engaging, informative, and entertaining throughout, with a special emphasis on humor and creativity in the opening and closing sections.
        """,
        agent=writer,
        expected_output="A blog post with an exceptionally witty introduction, at least 10 paragraphs, and a hilariously entertaining summary, following the specified markdown format and incorporating emojis creatively.",
        inputs={'formatted_output':task_report.output},
        output_file=output_markdown_file,
        timeout=6000
    )

    task_critique = AppendTask(
        description="""The output MUST have the following markdown format:
        ```
        ## [Witty Title] 🎉

        [Exceptionally humorous introduction with creative emoji use]

        ## 1. [Post Title] 🚀
        (If there is no corresponding link, you can not fill in)
        - Reddit:(https://www.reddit.com/r/LocalLLaMA/comments/example1.com)
        - Github:(https://github.com/example2.com)
        - Page:(https://papeg.ai/example3.com)
        - Huggingface(https://huggingface.ai/example4.com)....
        ....(More other links)
        - facts(To describe in detail)
        - Personal thoughts on how it connects to the overall theme of the newsletter
        - Description of how the project disrupted the industry
        - Help for users
        
        (If there are multiple related links, you can write multiple links.)
        (If there is no corresponding link, you can not fill in)
        ## 2. [Post Title] 🧠
        - Reddit:(https://www.reddit.com/r/LocalLLaMA/comments/example1.com)
        - Github:(https://github.com/example2.com)
        - Page:((https://papeg.ai/example3.com)
        - Huggingface(https://huggingface.ai/example4.com)....
        ....(More other links)
        - facts(To describe in detail)
        - Personal thoughts on how it connects to the overall theme of the newsletter
        - Description of how the project disrupted the industry
        - Help for users
        
        (If there are multiple related links, you can write multiple links.)
        (If there is no corresponding link, you can not fill in)
        ## 3. [Post Title] 🚀
        - Reddit:(https://www.reddit.com/r/LocalLLaMA/comments/example1.com)
        - Github:(https://github.com/example2.com)
        - Page:(https://papeg.ai/example3.com)
        - Huggingface(https://huggingface.ai/example4.com)
        ....(More other links)
        - facts(To describe in detail)
        - Personal thoughts on how it connects to the overall theme of the newsletter
        - Description of how the project disrupted the industry
        - Help for users
        ......

        ```
        [Vivid, memorable, and hilariously entertaining summary with creative emoji use]

        1. Make sure that it does and if it doesn't, rewrite it accordingly. 
        2. Ensure the introduction is witty and humorous, and the summary is vivid and memorable.
        3. Note that the links correspond to different platforms. For example, Reddit, Github, Huggingfacce, and so on,If there are errors, modify them
        4. Finally, there is no need to output the "feedback and criticism" section        """,
        agent=critic,
        expected_output="Give feedback and criticism on draft blog posts and make revisions, ensuring the specified markdown format is followed, including the witty introduction and vivid summary.",
        output_file=output_markdown_file,
        timeout=6000
    )

    return task_report, task_blog, task_critique
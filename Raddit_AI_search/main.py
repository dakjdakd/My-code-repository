import os
import time
from datetime import datetime
from dotenv import load_dotenv
from crewai import Crew, Process
from config import MODEL_NAME, OUTPUT_BASE_NAME
from agents import explorer, writer, critic
from tasks import create_tasks
from html_generator import generate_html
import agentops

load_dotenv()
agentops.init(os.getenv("AGENTOPS_API_KEY"))
# 定义输出目录
output_directory = os.path.join(os.path.dirname(__file__), "Reddit_news_everyday")
os.makedirs(output_directory, exist_ok=True)

# 更新输出文件路径
output_markdown_file = os.path.join(output_directory, f"{OUTPUT_BASE_NAME}.md")
output_html_file = os.path.join(output_directory, f"{OUTPUT_BASE_NAME}.html")

# 创建任务
task_report, task_blog, task_critique = create_tasks(output_markdown_file)


# Instantiate crew of agents
crew = Crew(
    agents=[explorer, writer, critic],
    tasks=[task_report, task_blog, task_critique],
    verbose=True,
    process=Process.sequential,
    timeout=18000
)

start_time = time.time()
start_datetime = datetime.now() 

result = crew.kickoff()

end_time = time.time()
end_datetime = datetime.now()
elapsed_time = end_time - start_time

# 记录结束时间并附加额外信息
with open(output_markdown_file, "a", encoding="utf-8") as file:
    file.write("\n")
    file.write("\n------------------------------------------------------------\n")
    file.write(f"程序开始运行时间: {start_datetime.strftime('%Y-%m-%d %H:%M:%S')}\n")
    file.write("\n------------------------------------------------------------\n")
    file.write(f"程序结束运行时间: {end_datetime.strftime('%Y-%m-%d %H:%M:%S')}\n")
    file.write("\n------------------------------------------------------------\n")
    file.write(f"整个运行过程使用了 {elapsed_time:.2f} 秒.\n")
    file.write("\n------------------------------------------------------------\n")
    file.write(f"本次程序运行使用的模型: {MODEL_NAME}\n")
    file.write("------------------------------------------------------------\n\n")

# 生成 HTML
generate_html(output_markdown_file, output_html_file)

# 删除 MD 文件
try:
    os.remove(output_markdown_file)
    print(f"已删除 Markdown 文件: {output_markdown_file}")
except FileNotFoundError:
    print(f"未找到要删除的文件: {output_markdown_file}")
except PermissionError:
    print(f"没有权限删除文件: {output_markdown_file}")

print(f"HTML 报告已保存至: {output_html_file}")
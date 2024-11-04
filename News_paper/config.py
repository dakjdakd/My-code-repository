import os
from dotenv import load_dotenv
from datetime import datetime

# 加载 .env 文件中的环境变量
load_dotenv()

# 选择要使用的模型名称
MODEL_NAME = os.getenv("MODEL_NAME", "glm-4-plus")

# 获取当前的日期和时间，格式化为"月日时分"
now = datetime.now()
OUTPUT_BASE_NAME = f"{now.strftime('%m月%d日%H时%M分')}的新闻摘要"

# 定义输出目录
OUTPUT_DIRECTORY = r"D:\cursor\News_paper\News"
os.makedirs(OUTPUT_DIRECTORY, exist_ok=True)  # 创建目录，如果不存在的话

# 更新输出文件路径
OUTPUT_MARKDOWN_FILE = os.path.join(OUTPUT_DIRECTORY, f"{OUTPUT_BASE_NAME}.md")
OUTPUT_HTML_FILE = os.path.join(OUTPUT_DIRECTORY, f"{OUTPUT_BASE_NAME}.html")
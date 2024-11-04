import os
import markdown2
import re
from datetime import datetime
import argparse

# 在这里指定默认的输入路径
DEFAULT_INPUT_PATH = r"D:\cursor\Raddit_report\Reddit_news_everyday\10月10日13时12分的Reddit_report.md"

def convert_md_to_html(md_file_path):
    # CSS 样式
    css = """
    <style>
        :root {
            --primary-color: #4a4a4a;
            --secondary-color: #0066cc;
            --background-color: #f4f4f4;
            --card-background: #ffffff;
        }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: var(--background-color);
            color: var(--primary-color);
            margin: 0;
            padding: 0;
            line-height: 1.6;
            transition: background-color 0.3s, color 0.3s;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }
        header {
            background-color: var(--secondary-color);
            color: white;
            text-align: center;
            padding: 1em;
        }
        h1 {
            margin: 0;
        }
        h2 {
            color: var(--secondary-color);
            border-bottom: 2px solid var(--secondary-color);
            padding-bottom: 10px;
            margin-top: 30px;
        }
        .card {
            background-color: var(--card-background);
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            margin-bottom: 20px;
            padding: 20px;
            transition: transform 0.3s ease;
        }
        .card:hover {
            transform: scale(1.05);
        }
        .card h3 {
            color: var(--secondary-color);
            margin-top: 0;
        }
        a {
            color: var(--secondary-color);
            text-decoration: none;
        }
        a:hover {
            text-decoration: underline;
        }
        .emoji {
            font-size: 1.5em;
            margin-right: 5px;
        }
        footer {
            text-align: center;
            margin-top: 40px;
            padding: 20px;
            background-color: var(--secondary-color);
            color: white;
        }
        @media (max-width: 600px) {
            .container {
                padding: 10px;
            }
        }
        
        /* 暗黑模式样式 */
        body.dark-mode {
            --primary-color: #e0e0e0;
            --secondary-color: #4da6ff;
            --background-color: #2c2c2c;
            --card-background: #3c3c3c;
        }
        body.dark-mode header,
        body.dark-mode footer {
            background-color: #1a1a1a;
        }
        body.dark-mode .card {
            background-color: var(--card-background);
        }
        #darkModeToggle {
            background-color: var(--secondary-color);
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            cursor: pointer;
            transition: background-color 0.3s;
        }
        #darkModeToggle:hover {
            background-color: #0052a3;
        }
        
        /* 新增的动画和交互样式 */
        @keyframes wave {
            50% { rotate: 10deg; }
        }
        
        @keyframes hover {
            from, to { translate: 0 -5%; }
            50% { translate: 0 5%; }
        }
        
        .intro {
            display: flex;
            justify-content: center;
            gap: 0.2em;
            font-size: 2em;
            margin-top: 20px;
        }
        
        .intro span {
            display: inline-block;
        }
        
        .intro span:first-child {
            transform-origin: right bottom;
            animation: wave 250ms 1s ease 3;
        }
        
        .intro span:last-child {
            animation: hover 500ms linear infinite;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        
        .fade-in {
            animation: fadeIn 1s ease-out;
        }
    </style>
    """

    # JavaScript 代码
    javascript = """
    <script>
        function toggleDarkMode() {
            document.body.classList.toggle('dark-mode');
            const button = document.getElementById('darkModeToggle');
            if (document.body.classList.contains('dark-mode')) {
                button.textContent = '切换到亮色模式';
            } else {
                button.textContent = '切换到暗色模式';
            }
        }

        // 平滑滚动
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
                document.querySelector(this.getAttribute('href')).scrollIntoView({
                    behavior: 'smooth'
                });
            });
        });
        
        // 新增的动画效果函数
        function addFadeInEffect() {
            const cards = document.querySelectorAll('.card');
            const observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        entry.target.classList.add('fade-in');
                        observer.unobserve(entry.target);
                    }
                });
            }, { threshold: 0.1 });
            
            cards.forEach(card => observer.observe(card));
        }
        
        // 页面加载完成后执行
        window.addEventListener('load', addFadeInEffect);
    </script>
    """

    def custom_markdown_to_html(md_content):
        pattern = r'(## .+?\n)(.+?)(?=\n## |\Z)'
        matches = re.findall(pattern, md_content, re.DOTALL)
        
        html_content = "<div class='container'>"
        for title, content in matches:
            html_title = markdown2.markdown(title.strip())
            html_content += f"<div class='card'>{html_title}{markdown2.markdown(content.strip())}</div>"
        
        html_content += "</div>"
        return html_content

    # 读取 Markdown 文件
    with open(md_file_path, "r", encoding="utf-8") as md_file:
        md_content = md_file.read()

    # 转换 Markdown 为 HTML
    html_content = custom_markdown_to_html(md_content)

    # 创建完整的 HTML 结构
    html_structure = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>AI新闻摘要</title>
        {css}
    </head>
    <body>
        <header>
            <h1>🚀 AI新闻摘要 🤖</h1>
            <button id="darkModeToggle" onclick="toggleDarkMode()">切换到暗色模式</button>
        </header>
        <div class="intro" aria-label="向下滚动查看更多">
            <span>👋</span>
            <span>⬇️</span>
        </div>
        {html_content}
        <footer>
            <p>生成于 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </footer>
        {javascript}
    </body>
    </html>
    """

    # 生成输出 HTML 文件路径
    output_dir = os.path.dirname(md_file_path)
    output_file_name = os.path.splitext(os.path.basename(md_file_path))[0] + ".html"
    output_html_file = os.path.join(output_dir, output_file_name)

    # 写入 HTML 文件
    with open(output_html_file, "w", encoding="utf-8") as html_file:
        html_file.write(html_structure)

    print(f"HTML 报告已保存至: {output_html_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="将Markdown文件转换为HTML报告")
    parser.add_argument("input_path", nargs='?', default=DEFAULT_INPUT_PATH, help="输入Markdown文件的路径")
    parser.add_argument("-o", "--output_path", help="输出HTML文件的路径(可选)")
    args = parser.parse_args()

    md_file_path = args.input_path
    
    if args.output_path:
        output_dir = os.path.dirname(args.output_path)
        output_file_name = os.path.basename(args.output_path)
    else:
        output_dir = os.path.dirname(md_file_path)
        output_file_name = os.path.splitext(os.path.basename(md_file_path))[0] + ".html"
    
    output_html_file = os.path.join(output_dir, output_file_name)
    
    convert_md_to_html(md_file_path)
    print(f"HTML 报告已保存至: {output_html_file}")
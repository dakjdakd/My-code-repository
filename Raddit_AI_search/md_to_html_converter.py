import os
import markdown2
import re
from datetime import datetime
import argparse

# 在这里指定默认的输入路径
DEFAULT_INPUT_PATH = r"C:\Users\MR\Desktop\book_study\LLM-Notes\11月05日17时50分的Reddit_report.md"

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
        
        /* 暗黑模样式 */
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
        
        .main-content {
            margin-bottom: 40px;
        }
        
        .program-info {
            background: linear-gradient(145deg, rgba(255, 255, 255, 0.1), rgba(255, 255, 255, 0.2));
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            border-radius: 20px;
            margin: 40px auto;
            max-width: 900px;
            padding: 30px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        .info-title {
            text-align: center;
            color: var(--secondary-color);
            font-size: 1.8em;
            margin-bottom: 30px;
            text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }
        
        .info-card {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            padding: 20px;
            background: rgba(255, 255, 255, 0.05);
            border-radius: 15px;
        }
        
        .info-item {
            display: flex;
            flex-direction: column;
            align-items: center;
            padding: 25px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 12px;
            transition: all 0.3s ease;
            text-align: center;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        .info-item:hover {
            transform: translateY(-5px);
            background: rgba(255, 255, 255, 0.15);
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
        }
        
        .info-item i {
            font-size: 24px;
            color: var(--secondary-color);
            margin-bottom: 15px;
        }
        
        .info-label {
            font-weight: bold;
            color: var(--secondary-color);
            margin: 8px 0;
            font-size: 0.9em;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        .info-value {
            color: var(--primary-color);
            font-size: 1.1em;
            margin-top: 5px;
        }
        
        /* 暗黑模式适配 */
        body.dark-mode .program-info {
            background: linear-gradient(145deg, rgba(0, 0, 0, 0.2), rgba(0, 0, 0, 0.3));
        }
        
        body.dark-mode .info-item {
            background: rgba(0, 0, 0, 0.2);
        }
        
        body.dark-mode .info-item:hover {
            background: rgba(0, 0, 0, 0.3);
        }
        
        /* 分隔线 */
        .content-divider {
            height: 2px;
            background: linear-gradient(to right, transparent, var(--secondary-color), transparent);
            margin: 40px auto;
            max-width: 80%;
            opacity: 0.3;
        }
        
        @media (max-width: 768px) {
            .info-card {
                grid-template-columns: 1fr;
            }
            
            .program-info {
                margin: 20px 10px;
                padding: 15px;
            }
            
            .info-item {
                padding: 15px;
            }
        }

        /* 内容区域样式 */
        .content-section {
            background: rgba(255, 255, 255, 0.02);
            border-radius: 20px;
            padding: 30px;
            margin-bottom: 40px;
        }

        /* 分隔区域样式 */
        .section-divider {
            position: relative;
            height: 80px;
            margin: 40px 0;
            display: flex;
            align-items: center;
            justify-content: center;
        }

        .section-divider::before {
            content: '';
            position: absolute;
            width: 100%;
            height: 2px;
            background: linear-gradient(90deg, 
                transparent 0%, 
                var(--secondary-color) 20%, 
                var(--secondary-color) 80%, 
                transparent 100%
            );
            opacity: 0.3;
        }

        /* 卡片样式优化 */
        .card {
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 15px;
            padding: 25px;
            margin-bottom: 25px;
            transition: all 0.3s ease;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }

        .card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 15px rgba(0, 0, 0, 0.2);
        }

        /* 程序运行信息样式优化 */
        .program-info {
            background: linear-gradient(145deg, 
                rgba(255, 255, 255, 0.05) 0%, 
                rgba(255, 255, 255, 0.1) 100%
            );
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 30px;
            margin-top: 20px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        }

        .info-title {
            text-align: center;
            color: var(--secondary-color);
            font-size: 1.8em;
            margin-bottom: 30px;
            text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            position: relative;
            padding-bottom: 15px;
        }

        .info-title::after {
            content: '';
            position: absolute;
            bottom: 0;
            left: 50%;
            transform: translateX(-50%);
            width: 100px;
            height: 3px;
            background: var(--secondary-color);
            border-radius: 2px;
        }

        .info-card {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 25px;
            padding: 20px;
        }

        .info-item {
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 15px;
            padding: 25px;
            text-align: center;
            transition: all 0.3s ease;
        }

        .info-item:hover {
            transform: translateY(-5px);
            background: rgba(255, 255, 255, 0.1);
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
        }

        .info-item i {
            font-size: 28px;
            color: var(--secondary-color);
            margin-bottom: 15px;
            transition: transform 0.3s ease;
        }

        .info-item:hover i {
            transform: scale(1.2);
        }

        .info-label {
            font-weight: bold;
            color: var(--secondary-color);
            margin: 10px 0;
            font-size: 0.9em;
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        .info-value {
            color: var(--primary-color);
            font-size: 1.1em;
            margin-top: 8px;
        }

        /* 暗黑模式适配 */
        body.dark-mode .content-section {
            background: rgba(0, 0, 0, 0.2);
        }

        body.dark-mode .program-info {
            background: linear-gradient(145deg, 
                rgba(0, 0, 0, 0.2) 0%, 
                rgba(0, 0, 0, 0.3) 100%
            );
        }

        body.dark-mode .card,
        body.dark-mode .info-item {
            background: rgba(0, 0, 0, 0.2);
            border-color: rgba(255, 255, 255, 0.05);
        }

        body.dark-mode .card:hover,
        body.dark-mode .info-item:hover {
            background: rgba(0, 0, 0, 0.3);
        }

        /* 响应式布局优化 */
        @media (max-width: 768px) {
            .content-section {
                padding: 15px;
            }
            
            .info-card {
                grid-template-columns: 1fr;
            }
            
            .program-info {
                margin: 20px 10px;
                padding: 20px;
            }
            
            .section-divider {
                height: 60px;
                margin: 30px 0;
            }
        }

        /* 新增返回顶部按钮样式 */
        .back-to-top {
            position: fixed;
            bottom: 30px;
            right: 30px;
            background: var(--secondary-color);
            color: white;
            width: 50px;
            height: 50px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            opacity: 0;
            transition: all 0.3s ease;
            z-index: 1000;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
        }
        
        .back-to-top.visible {
            opacity: 1;
        }
        
        .back-to-top:hover {
            transform: translateY(-5px);
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
        }
        
        /* 进度条样式 */
        .progress-bar {
            position: fixed;
            top: 0;
            left: 0;
            width: 0%;
            height: 3px;
            background: linear-gradient(to right, #4CAF50, #2196F3);
            z-index: 1001;
            transition: width 0.2s ease;
        }
        
        /* 目录导航样式 */
        .toc {
            position: fixed;
            left: 20px;
            top: 50%;
            transform: translateY(-50%);
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            padding: 20px;
            border-radius: 15px;
            max-height: 80vh;
            overflow-y: auto;
            z-index: 100;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.1);
            display: none;
        }
        
        .toc.visible {
            display: block;
        }
        
        .toc-list {
            list-style: none;
            padding: 0;
            margin: 0;
        }
        
        .toc-item {
            margin: 10px 0;
            opacity: 0.7;
            transition: all 0.3s ease;
        }
        
        .toc-item:hover {
            opacity: 1;
            transform: translateX(5px);
        }
        
        .toc-item.active {
            opacity: 1;
            color: var(--secondary-color);
            font-weight: bold;
        }
        
        .toc-toggle {
            position: fixed;
            left: 20px;
            top: 50%;
            transform: translateY(-50%);
            background: var(--secondary-color);
            color: white;
            width: 40px;
            height: 40px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            z-index: 101;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
            transition: all 0.3s ease;
        }
        
        .toc-toggle:hover {
            transform: translateY(-50%) scale(1.1);
        }
        
        /* 总结卡片样式 */
        .summary-card {
            background: linear-gradient(145deg, 
                rgba(255, 255, 255, 0.1) 0%, 
                rgba(255, 255, 255, 0.15) 100%
            );
            border: 1px solid rgba(255, 255, 255, 0.2);
            margin-top: 40px;
            padding: 30px;
        }

        .summary-card h2 {
            color: var(--secondary-color);
            text-align: center;
            font-size: 1.8em;
            margin-bottom: 25px;
            border-bottom: none;
            text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }

        .summary-card p {
            font-size: 1.1em;
            line-height: 1.8;
            text-align: justify;
        }

        @media (max-width: 1200px) {
            .toc, .toc-toggle {
                display: none;
            }
        }

        /* 链接样式 */
        .card a {
            color: #0066cc !important;
            text-decoration: none !important;
            padding: 2px 4px;
            border-radius: 3px;
            transition: all 0.3s ease;
            display: inline-block;
            background-color: rgba(0, 102, 204, 0.05);
            margin: 0 2px;
            cursor: pointer;
            position: relative;
        }
        
        .card a:hover {
            background-color: rgba(0, 102, 204, 0.1);
            color: #0052a3 !important;
            transform: translateY(-1px);
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }
        
        /* 列表项中的链接 */
        .card li a {
            display: inline-block;
            margin: 0 4px;
        }
        
        /* 外部链接图标 */
        .card a[target="_blank"]::after {
            content: '↗️';
            font-size: 0.8em;
            margin-left: 4px;
            opacity: 0.7;
            vertical-align: text-top;
        }
        
        /* 确保链接在暗色模式下也可见 */
        body.dark-mode .card a {
            color: #4da6ff !important;
        }
        
        body.dark-mode .card a:hover {
            color: #66b3ff !important;
            background-color: rgba(77, 166, 255, 0.1);
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
        window.addEventListener('load', () => {
            addFadeInEffect();
            generateToc();
            updateTocActiveState();
        });

        // 返回顶部功能
        const backToTop = document.querySelector('.back-to-top');
        window.addEventListener('scroll', () => {
            if (window.scrollY > 300) {
                backToTop.classList.add('visible');
            } else {
                backToTop.classList.remove('visible');
            }
            
            // 更新进度条
            const winScroll = document.body.scrollTop || document.documentElement.scrollTop;
            const height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
            const scrolled = (winScroll / height) * 100;
            document.querySelector('.progress-bar').style.width = scrolled + '%';
            
            // 更新目录激活状态
            updateTocActiveState();
        });

        // 返回顶部点击事件
        document.querySelector('.back-to-top').addEventListener('click', () => {
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });
        
        // 目录功能
        function generateToc() {
            const headings = document.querySelectorAll('.card h2');
            const tocList = document.querySelector('.toc-list');
            
            headings.forEach((heading, index) => {
                const li = document.createElement('li');
                li.classList.add('toc-item');
                li.innerHTML = `<a href="#heading-${index}">${heading.textContent}</a>`;
                tocList.appendChild(li);
                
                // 添加ID到标题
                heading.id = `heading-${index}`;
            });
        }
        
        function updateTocActiveState() {
            const headings = document.querySelectorAll('.card h2');
            const tocItems = document.querySelectorAll('.toc-item');
            
            headings.forEach((heading, index) => {
                const rect = heading.getBoundingClientRect();
                if (rect.top >= 0 && rect.top <= window.innerHeight * 0.5) {
                    tocItems.forEach(item => item.classList.remove('active'));
                    tocItems[index].classList.add('active');
                }
            });
        }
        
        // 切换目录显示
        document.querySelector('.toc-toggle').addEventListener('click', () => {
            document.querySelector('.toc').classList.toggle('visible');
        });
    </script>
    """
    
    
    
    def custom_markdown_to_html(md_content):
        def process_links(content):
            # 处理链接格式
            pattern = r'\[([^\]]+)\]\((https?://[^\)]+)\)'
            def replace_link(match):
                text = match.group(1).strip()
                url = match.group(2).strip()
                return f'<a href="{url}" target="_blank" rel="noopener noreferrer">{text}</a>'
            
            return re.sub(pattern, replace_link, content)

        # 分离主要内容和程序运行信息
        main_content, run_info = split_content(md_content)
        
        html_content = "<div class='container main-content'>"
        html_content += "<div class='content-section'>"
        
        pattern = r'(## .+?\n)(.+?)(?=\n## |\Z)'
        matches = re.findall(pattern, main_content, re.DOTALL)
        for title, content in matches:
            # 处理内容中的链接
            processed_content = process_links(content)
            html_title = markdown2.markdown(title.strip())
            html_content += f"<div class='card'>{html_title}{markdown2.markdown(processed_content)}</div>"
        
        html_content += "</div>"
        
        # 添加分隔区域
        html_content += "<div class='section-divider'></div>"
        
        # 添加程序运行信息区块
        if run_info:
            html_content += """
            <div class='program-info'>
                <h2 class='info-title'>程序运行信息</h2>
                <div class='info-card'>
                    """ + run_info + """
                </div>
            </div>
            """
        
        html_content += "</div>"
        return html_content

    def split_content(md_content):
        # 使用更精确的分割方式
        run_info_pattern = r'程序开始运行时间: (.*?)\n.*?程序结束运行时间: (.*?)\n.*?整个运行过程使用了 (.*?)秒.*?本次程序运行使用的模型: (.*?)(?:\n|$)'
        match = re.search(run_info_pattern, md_content, re.DOTALL)
        
        if match:
            main_content = md_content[:match.start()].strip()
            run_info = f"""
                <div class='info-item'>
                    <i class='fas fa-play-circle'></i>
                    <span class='info-label'>开始时间</span>
                    <span class='info-value'>{match.group(1)}</span>
                </div>
                <div class='info-item'>
                    <i class='fas fa-stop-circle'></i>
                    <span class='info-label'>结束时间</span>
                    <span class='info-value'>{match.group(2)}</span>
                </div>
                <div class='info-item'>
                    <i class='fas fa-clock'></i>
                    <span class='info-label'>运行时长</span>
                    <span class='info-value'>{match.group(3)} 秒</span>
                </div>
                <div class='info-item'>
                    <i class='fas fa-microchip'></i>
                    <span class='info-label'>使用模型</span>
                    <span class='info-value'>{match.group(4)}</span>
                </div>
            """
        else:
            main_content = md_content
            run_info = ""
        
        return main_content, run_info

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
        <link rel="icon" type="image/png" href="../assets/favicon.png">
        <title>AI新闻摘要</title>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
        {css}
        {get_shader()}
    </head>
    <body>
        <div class="progress-bar"></div>
        <div class="toc-toggle">
            <i class="fas fa-list"></i>
        </div>
        <nav class="toc">
            <ul class="toc-list"></ul>
        </nav>
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
        <div class="back-to-top">
            <i class="fas fa-arrow-up"></i>
        </div>
        {javascript}
        {get_renderer_js()}
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

# ... 前面的代码保持不变 ...

def get_shader():
    return """
    <script type="x-shader/x-fragment">#version 300 es
    precision highp float;
    out vec4 O;
    uniform float time;
    uniform vec2 resolution;
    #define FC gl_FragCoord.xy
    #define R resolution
    #define T (time * 0.15)
    #define hue(a) (.5+.5*cos(6.3*(a)+vec3(0,83,21)))
    float rnd(float a) {
        vec2 p=fract(a*vec2(12.9898,78.233)); p+=dot(p,p*345.);
        return fract(p.x*p.y);
    }
    vec3 pattern(vec2 uv) {
        vec3 col=vec3(0);
        for (float i=.0; i++<15.;) {
            float a=rnd(i);
            vec2 n=vec2(a,fract(a*34.56)), p=sin(n*(T+7.)+T*.5);
            float d=dot(uv-p,uv-p);
            col+=.0006/d*hue(dot(uv,uv)+i*.125+T);
        }
        return col * 0.8;
    }
    void main(void) {
        vec2 uv=(FC-.5*R)/min(R.x,R.y);
        vec3 col=vec3(0);
        float s=2.4,
        a=atan(uv.x,uv.y),
        b=length(uv);
        uv=vec2(a*5./6.28318,.05/tan(b)+T);
        uv=fract(uv)-.5;
        col+=pattern(uv*s);
        O=vec4(col,1);
    }</script>
    """

def get_renderer_js():
    return """
    <script>
    window.onload = init;
    function init() {
        let renderer, canvas;
        const dpr = Math.max(1, .5*devicePixelRatio);
        
        canvas = document.createElement("canvas");
        canvas.style.position = 'fixed';
        canvas.style.top = '0';
        canvas.style.left = '0';
        canvas.style.width = '100%';
        canvas.style.height = '100%';
        canvas.style.zIndex = '-1';
        document.body.insertBefore(canvas, document.body.firstChild);
        
        const resize = () => {
            const { innerWidth: width, innerHeight: height } = window;
            canvas.width = width * dpr;
            canvas.height = height * dpr;
            if (renderer) {
                renderer.updateScale(dpr);
            }
        };
        
        const source = document.querySelector("script[type='x-shader/x-fragment']").textContent;
        canvas.style.userSelect = "none";
        renderer = new Renderer(canvas, dpr);
        renderer.setup();
        renderer.init();
        resize();
        if (renderer.test(source) === null) {
            renderer.updateShader(source);
        }
        window.onresize = resize;
        const loop = (now) => {
            renderer.render(now);
            requestAnimationFrame(loop);
        };
        loop(0);
    }
    
    class Renderer {
        #vertexSrc = "#version 300 es\\nprecision highp float;\\nin vec4 position;\\nvoid main(){gl_Position=position;}";
        #fragmtSrc = "#version 300 es\\nprecision highp float;\\nout vec4 O;\\nuniform float time;\\nuniform vec2 resolution;\\nvoid main() {\\n\\tvec2 uv=gl_FragCoord.xy/resolution;\\n\\tO=vec4(uv,sin(time)*.5+.5,1);\\n}";
        #vertices = [-1, 1, -1, -1, 1, 1, 1, -1];
        
        constructor(canvas, scale) {
            this.canvas = canvas;
            this.scale = scale;
            this.gl = canvas.getContext("webgl2");
            this.gl.viewport(0, 0, canvas.width * scale, canvas.height * scale);
            this.shaderSource = this.#fragmtSrc;
            this.mouseCoords = [0, 0];
            this.pointerCoords = [0, 0];
            this.nbrOfPointers = 0;
        }

        get defaultSource() { 
            return this.#fragmtSrc;
        }

        updateShader(source) {
            this.reset();
            this.shaderSource = source;
            this.setup();
            this.init();
        }

        updateScale(scale) {
            this.scale = scale;
            this.gl.viewport(0, 0, this.canvas.width * scale, this.canvas.height * scale);
        }

        compile(shader, source) {
            const gl = this.gl;
            gl.shaderSource(shader, source);
            gl.compileShader(shader);
            if (!gl.getShaderParameter(shader, gl.COMPILE_STATUS)) {
                console.error(gl.getShaderInfoLog(shader));
            }
        }

        test(source) {
            let result = null;
            const gl = this.gl;
            const shader = gl.createShader(gl.FRAGMENT_SHADER);
            gl.shaderSource(shader, source);
            gl.compileShader(shader);
            if (!gl.getShaderParameter(shader, gl.COMPILE_STATUS)) {
                result = gl.getShaderInfoLog(shader);
            }
            gl.deleteShader(shader);
            return result;
        }

        reset() {
            const gl = this.gl;
            if (this.program) {
                if (this.vs) {
                    gl.detachShader(this.program, this.vs);
                    gl.deleteShader(this.vs);
                }
                if (this.fs) {
                    gl.detachShader(this.program, this.fs);
                    gl.deleteShader(this.fs);
                }
                gl.deleteProgram(this.program);
            }
        }

        setup() {
            const gl = this.gl;
            this.vs = gl.createShader(gl.VERTEX_SHADER);
            this.fs = gl.createShader(gl.FRAGMENT_SHADER);
            this.compile(this.vs, this.#vertexSrc);
            this.compile(this.fs, this.shaderSource);
            this.program = gl.createProgram();
            gl.attachShader(this.program, this.vs);
            gl.attachShader(this.program, this.fs);
            gl.linkProgram(this.program);
        }

        init() {
            const gl = this.gl;
            this.buffer = gl.createBuffer();
            gl.bindBuffer(gl.ARRAY_BUFFER, this.buffer);
            gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(this.#vertices), gl.STATIC_DRAW);
            const position = gl.getAttribLocation(this.program, "position");
            gl.enableVertexAttribArray(position);
            gl.vertexAttribPointer(position, 2, gl.FLOAT, false, 0, 0);
            this.program.resolution = gl.getUniformLocation(this.program, "resolution");
            this.program.time = gl.getUniformLocation(this.program, "time");
        }

        render(now = 0) {
            const gl = this.gl;
            gl.clearColor(0, 0, 0, 1);
            gl.clear(gl.COLOR_BUFFER_BIT);
            gl.useProgram(this.program);
            gl.bindBuffer(gl.ARRAY_BUFFER, this.buffer);
            gl.uniform2f(this.program.resolution, this.canvas.width, this.canvas.height);
            gl.uniform1f(this.program.time, now * 0.001);
            gl.drawArrays(gl.TRIANGLE_STRIP, 0, 4);
        }
    }
    </script>
    """

# ... 其余代码保持不变 ...

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
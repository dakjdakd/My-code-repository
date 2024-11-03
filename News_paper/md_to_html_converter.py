import os
import markdown2
from datetime import datetime
from config import OUTPUT_DIRECTORY

def convert_md_to_html(md_file_path, model_name):
    # 检查文件是否存在
    if not os.path.exists(md_file_path):
        print(f"错误：文件 {md_file_path} 不存在。")
        return

    # 读取Markdown文件内容
    with open(md_file_path, 'r', encoding='utf-8') as md_file:
        md_content = md_file.read()

    # 转换Markdown为HTML
    html_content = markdown2.markdown(md_content)

    # 生成HTML文件名
    md_filename = os.path.basename(md_file_path)
    html_filename = os.path.splitext(md_filename)[0] + '.html'
    html_file_path = os.path.join(OUTPUT_DIRECTORY, html_filename)

    # 获取当前时间
    now = datetime.now()
    start_datetime = now

    # CSS 代码
    css = """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&display=swap');
        @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap');
        
        :root {
            --x: 0;
            --y: 0;
            --bg-color: #f0f2f5;
            --grid-color: rgba(0, 0, 0, 0.1);
            --grid-size: 40px;
        }
        
        body {
            font-family: 'Roboto', sans-serif;
            line-height: 1.6;
            color: #333;
            margin: 0;
            padding: 0;
            background-color: var(--bg-color);
            transition: all 0.3s ease;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            align-items: center;
            background-image: 
                linear-gradient(var(--grid-color) 1px, transparent 1px),
                linear-gradient(90deg, var(--grid-color) 1px, transparent 1px);
            background-size: var(--grid-size) var(--grid-size);
            background-position: 0 0, 0 0;
            background-attachment: fixed;
        }
        
        body::before {
            content: '';
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: radial-gradient(circle at 50% 50%, transparent 0%, var(--bg-color) 100%);
            z-index: 1;
            pointer-events: none;
        }
        
        .container {
            max-width: 800px;
            margin: 40px auto;
            padding: 20px;
            background-color: #ffffff;
            border-radius: 8px;
            box-shadow: 0 0 20px rgba(0,0,0,0.1);
            transition: all 0.3s ease;
            position: relative;
            z-index: 2;
        }
        
        h1, h2, h3 {
            color: #2c3e50;
            margin-top: 30px;
            transition: all 0.3s ease;
        }
        
        h1 {
            border-bottom: 2px solid #3498db;
            padding-bottom: 10px;
            font-size: 2.5em;
            text-align: center;
        }
        
        h2 {
            border-bottom: 1px solid #bdc3c7;
            padding-bottom: 5px;
            font-size: 2em;
        }
        
        h3 {
            color: #16a085;
            font-size: 1.5em;
        }
        
        p {
            margin-bottom: 15px;
            animation: fadeIn 0.5s ease-in-out;
        }
        
        a {
            color: #3498db;
            text-decoration: none;
            transition: all 0.3s ease;
        }
        
        a:hover {
            color: #2980b9;
            text-decoration: underline;
        }
        
        .meta-info {
            background-color: #ecf0f1;
            border-radius: 5px;
            padding: 15px;
            margin-top: 30px;
            font-size: 0.9em;
            color: #7f8c8d;
            transition: all 0.3s ease;
        }
        
        .meta-info p {
            margin: 5px 0;
        }
        
        .dark-mode {
            --bg-color: #1a1a1a;
            --grid-color: rgba(255, 255, 255, 0.1);
            color: #ecf0f1;
        }
        
        .dark-mode .container {
            background-color: #2c3e50;
            box-shadow: 0 0 20px rgba(255,255,255,0.1);
        }
        
        .dark-mode h1, .dark-mode h2, .dark-mode h3 {
            color: #3498db;
        }
        
        .dark-mode a {
            color: #5dade2;
        }
        
        .dark-mode .meta-info {
            background-color: #34495e;
            color: #bdc3c7;
        }
        
        #darkModeToggle {
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 10px 20px;
            background-color: #3498db;
            color: #ffffff;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        
        #darkModeToggle:hover {
            background-color: #2980b9;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        
        @media (max-width: 600px) {
            .container {
                margin: 20px;
                padding: 15px;
            }
            h1 { font-size: 2em; }
            h2 { font-size: 1.5em; }
            h3 { font-size: 1.2em; }
        }
        
        .card {
            width: 600px;
            aspect-ratio: 2 / 1.1;
            max-height: calc(100vh - 2rem);
            position: relative;
            overflow: hidden;
            max-width: calc(100% - 2rem);
            margin: 20px auto;
        }
        
        .assets {
            position: absolute;
            inset: 0;
            border-radius: 4em;
            overflow: hidden;
        }
        
        .assets > img {
            position: absolute;
            top: 0;
            left: 50%;
            translate: -50% 0;
            height: 100%;
            width: 660px;
            object-fit: cover;
            object-position: center 43%;
            user-select: none;
            pointer-events: none;
        }
        
        .assets > img:first-of-type {
            filter: saturate(1.5) brightness(0.9);
            object-position: calc(-50% + (var(--x) * 30px)) calc(43% + (var(--y) * -20px));
        }
        
        .assets > img:last-of-type {
            object-position: calc(-50% + (var(--x) * 40px)) calc(43% + (var(--y) * -40px));
        }
        
        .assets h3 {
            position: absolute;
            left: 50%;
            top: 6%;
            margin: 0;
            font-size: 8rem;
            translate: -50% 0;
            text-transform: uppercase;
            font-family: 'Bebas Neue', sans-serif;
            color: white;
            translate: calc(-50% + (var(--x) * -30px)) calc(var(--y) * -20px);
        }
        
        .card-content {
            min-height: 32%;
            position: absolute;
            bottom: 0;
            width: 100%;
            color: white;
            display: grid;
            gap: 0.2rem;
            place-items: center;
            align-content: center;
            padding-bottom: 0.5rem;
            z-index: 2;
        }
        
        .card-content svg {
            width: 20px;
        }
        
        .card-content p {
            margin: 0;
            display: flex;
            align-items: center;
            gap: 0.5rem;
            font-size: 1.2rem;
            position: relative;
        }
        
        .card-content p:first-of-type::after {
            content: '';
            position: absolute;
            bottom: calc(100% + 1rem);
            left: 50%;
            width: 6ch;
            background: white;
            height: 1px;
            translate: -50% 0;
        }
        
        .card-content p:last-of-type {
            opacity: 0.8;
        }
        
        .blur {
            --layers: 5;
            position: absolute;
            inset: 0;
        }
        
        .blur .layer {
            --blur: calc(
                sin(((var(--layers) - var(--index)) / var(--layers)) * 90deg) * 30
            );
            --stop: calc(
                sin(((var(--index)) / var(--layers)) * 90deg) * 15
            );
            position: absolute;
            inset: 0;
            background: hsl(0 0% 60% / 0.05);
            backdrop-filter: blur(calc(var(--blur) * 1px));
            mask: radial-gradient(
                150% 130% at 45% 90%,
                #fff 15%,
                #0000 calc((15 + var(--stop)) * 1%)
            );
        }
    </style>
    """

    # JavaScript 代码
    js = """
    <script src="https://cdn.skypack.dev/gsap@3.12.0"></script>
    <script>
    function toggleDarkMode() {
        const body = document.body;
        const button = document.getElementById('darkModeToggle');
        body.classList.toggle('dark-mode');
        if (body.classList.contains('dark-mode')) {
            button.textContent = '切换到浅色模式';
        } else {
            button.textContent = '切换到深色模式';
        }
    }

    function smoothScroll(target) {
        const element = document.querySelector(target);
        window.scrollTo({
            top: element.offsetTop,
            behavior: 'smooth'
        });
    }

    const UPDATE = ({ x, y }) => {
      gsap.set(document.documentElement, {
        '--x': gsap.utils.mapRange(0, window.innerWidth, -1, 1, x),
        '--y': gsap.utils.mapRange(0, window.innerHeight, -1, 1, y),
      })
    }

    window.addEventListener('mousemove', UPDATE)

    const handleOrientation = ({ beta, gamma }) => {
      const isLandscape = window.matchMedia('(orientation: landscape)').matches
      gsap.set(document.documentElement, {
        '--x': gsap.utils.clamp(-1, 1, isLandscape ? gsap.utils.mapRange(-45, 45, -1, 1, beta) : gsap.utils.mapRange(-45, 45, -1, 1, gamma)),
        '--y': gsap.utils.clamp(-1, 1, isLandscape ? gsap.utils.mapRange(20, 70, 1, -1, Math.abs(gamma)) : gsap.utils.mapRange(20, 70, 1, -1, beta)),
      })
    }

    const START = () => {
      if (
        DeviceOrientationEvent?.requestPermission
      ) {
        Promise.all([
          DeviceOrientationEvent.requestPermission(),
        ]).then((results) => {
          if (results.every((result) => result === "granted")) {
            window.addEventListener("deviceorientation", handleOrientation);
          }
        });
      } else {
        window.addEventListener("deviceorientation", handleOrientation);
      }
    };
    document.body.addEventListener('click', START, { once: true })
    </script>
    """

    html_structure = f"""
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>新闻摘要</title>
        {css}
    </head>
    <body>
        <button id="darkModeToggle" onclick="toggleDarkMode()">切换到深色模式</button>
        <div class="card">
            <div class="assets">
                <img src="https://assets.codepen.io/605876/do-not-copy-osaka-sky.jpeg" alt="" />
                <h3>新闻摘要</h3>
                <img src="https://assets.codepen.io/605876/do-not-copy-osaka-tower.png" alt="" />
            </div>
            <div class="blur">
                <div class="layer" style="--index:1;"></div>
                <div class="layer" style="--index:2;"></div>
                <div class="layer" style="--index:3;"></div>
                <div class="layer" style="--index:4;"></div>
                <div class="layer" style="--index:5;"></div>
            </div>
            <div class="card-content">
                <p>
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="w-6 h-6">
                        <path d="M15.75 8.25a.75.75 0 0 1 .75.75c0 1.12-.492 2.126-1.27 2.812a.75.75 0 1 1-.992-1.124A2.243 2.243 0 0 0 15 9a.75.75 0 0 1 .75-.75Z" />
                        <path fill-rule="evenodd" d="M12 2.25c-5.385 0-9.75 4.365-9.75 9.75s4.365 9.75 9.75 9.75 9.75-4.365 9.75-9.75S17.385 2.25 12 2.25ZM4.575 15.6a8.25 8.25 0 0 0 9.348 4.425 1.966 1.966 0 0 0-1.84-1.275.983.983 0 0 1-.97-.822l-.073-.437c-.094-.565.25-1.11.8-1.267l.99-.282c.427-.123.783-.418.982-.816l.036-.073a1.453 1.453 0 0 1 2.328-.377L16.5 15h.628a2.25 2.25 0 0 1 1.983 1.186 8.25 8.25 0 0 0-6.345-12.4c.044.262.18.503.389.676l1.068.89c.442.369.535 1.01.216 1.49l-.51.766a2.25 2.25 0 0 1-1.161.886l-.143.048a1.107 1.107 0 0 0-.57 1.664c.369.555.169 1.307-.427 1.605L9 13.125l.423 1.059a.956.956 0 0 1-1.652.928l-.679-.906a1.125 1.125 0 0 0-1.906.172L4.575 15.6Z" clip-rule="evenodd" />
                    </svg>
                    <span>今日热点</span>
                </p>
                <p>{start_datetime.strftime('%Y-%m-%d')}</p>
            </div>
        </div>
        <div class="container">
            {html_content}
        </div>
        {js}
    </body>
    </html>
    """

    # 写入HTML文件
    with open(html_file_path, "w", encoding="utf-8") as html_file:
        html_file.write(html_structure)

    print(f"HTML 文件已生成。路径：{html_file_path}")

if __name__ == "__main__":
    # 直接在代码中指定 Markdown 文件路径
    md_file_path = r"D:\cursor\News_paper\News\10月11日18时53分的新闻摘要.md"
    convert_md_to_html(md_file_path, "glm-4-plus")
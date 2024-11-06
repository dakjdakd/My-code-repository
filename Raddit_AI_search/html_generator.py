import markdown2
import re
from config import OUTPUT_BASE_NAME, MODEL_NAME
from datetime import datetime

class HTMLGenerator:
    @staticmethod
    def get_css():
        return """
        <style>
            :root {
                --primary-color: #4a4a4a;
                --secondary-color: #0066cc;
                --background-color: #f4f4f4;
                --card-background: #ffffff;
                --header-footer-bg: linear-gradient(135deg, rgba(0, 102, 204, 0.85), rgba(0, 82, 164, 0.85));
                --header-footer-shadow: 0 2px 20px rgba(0, 0, 0, 0.1);
            }
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background-color: var(--background-color);
                color: var(--primary-color);
                margin: 0;
                padding: 0;
                line-height: 1.6;
                transition: background-color 0.3s, color 0.3s;
                min-height: 100vh;
                display: flex;
                flex-direction: column;
            }
            .container {
                max-width: 800px;
                margin: 2em auto;
                padding: 20px;
                position: relative;
                z-index: 1;
                background: rgba(244, 244, 244, 0.9);
                border-radius: 15px;
                backdrop-filter: blur(10px);
                -webkit-backdrop-filter: blur(10px);
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
            }
            header {
                background: var(--header-footer-bg);
                color: white;
                text-align: center;
                padding: 1.5em 1em;
                position: relative;
                z-index: 1;
                backdrop-filter: blur(10px);
                -webkit-backdrop-filter: blur(10px);
                box-shadow: var(--header-footer-shadow);
                border-bottom: 1px solid rgba(255, 255, 255, 0.1);
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
                background: rgba(255, 255, 255, 0.9);
                border-radius: 12px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
                margin-bottom: 20px;
                padding: 25px;
                transition: all 0.3s ease;
                border: 1px solid rgba(0, 0, 0, 0.05);
                transform-origin: center;
                transition: all 0.4s cubic-bezier(0.165, 0.84, 0.44, 1);
            }
            .card:hover {
                transform: translateY(-8px) scale(1.01);
                box-shadow: 0 15px 30px rgba(0, 0, 0, 0.15);
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
                background: var(--header-footer-bg);
                color: white;
                text-align: center;
                padding: 1.5em 1em;
                position: relative;
                z-index: 1;
                backdrop-filter: blur(10px);
                -webkit-backdrop-filter: blur(10px);
                box-shadow: var(--header-footer-shadow);
                border-top: 1px solid rgba(255, 255, 255, 0.1);
                margin-top: auto;
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
                --header-footer-bg: linear-gradient(135deg, rgba(26, 26, 26, 0.95), rgba(38, 38, 38, 0.95));
            }
            body.dark-mode .container {
                background: rgba(44, 44, 44, 0.9);
            }
            body.dark-mode .card {
                background: rgba(60, 60, 60, 0.9);
                border: 1px solid rgba(255, 255, 255, 0.05);
            }
            body.dark-mode header,
            body.dark-mode footer {
                background: rgba(26, 26, 26, 0.9);
            }
            #darkModeToggle {
                background: rgba(255, 255, 255, 0.15);
                color: white;
                border: 1px solid rgba(255, 255, 255, 0.2);
                padding: 8px 16px;
                border-radius: 20px;
                cursor: pointer;
                transition: all 0.3s ease;
                backdrop-filter: blur(5px);
                -webkit-backdrop-filter: blur(5px);
            }
            #darkModeToggle:hover {
                background: rgba(255, 255, 255, 0.25);
                transform: translateY(-2px);
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

            /* 新增的内容区域和程序信息样式 */
            .content-section {
                background: rgba(255, 255, 255, 0.02);
                border-radius: 20px;
                padding: 30px;
                margin-bottom: 40px;
            }

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

            .program-info {
                background: linear-gradient(145deg, 
                    rgba(255, 255, 255, 0.05) 0%, 
                    rgba(255, 255, 255, 0.1) 100%
                );
                border: 1px solid rgba(255, 255, 255, 0.1);
                backdrop-filter: blur(10px);
                -webkit-backdrop-filter: blur(10px);
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
                grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
                gap: 25px;
                padding: 20px;
                justify-items: center;
            }

            .info-item {
                background: rgba(255, 255, 255, 0.05);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 15px;
                padding: 25px;
                text-align: center;
                transition: all 0.3s ease;
                position: relative;
                overflow: hidden;
                min-width: 220px;
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
                font-family: 'Consolas', monospace;
                letter-spacing: 0.5px;
                white-space: nowrap;
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

            body.dark-mode .info-item {
                background: rgba(0, 0, 0, 0.2);
            }

            body.dark-mode .info-item:hover {
                background: rgba(0, 0, 0, 0.3);
            }

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

            /* 总结卡片样式 */
            .summary-card {
                background: linear-gradient(145deg, 
                    rgba(var(--secondary-color-rgb), 0.05) 0%,
                    rgba(var(--secondary-color-rgb), 0.1) 100%
                );
                border: 2px solid rgba(var(--secondary-color-rgb), 0.1);
                margin-top: 40px;
                padding: 30px;
            }

            .summary-card h2 {
                text-align: center;
                font-size: 2em;
                margin-bottom: 30px;
                color: var(--secondary-color);
                text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            }

            .summary-card p {
                font-size: 1.1em;
                line-height: 1.8;
                text-align: justify;
            }

            /* 暗黑模式适 */
            body.dark-mode .summary-card {
                background: linear-gradient(145deg, 
                    rgba(0, 0, 0, 0.2) 0%, 
                    rgba(0, 0, 0, 0.3) 100%
                );
                border-color: rgba(255, 255, 255, 0.1);
            }

            .summary-card:hover {
                transform: translateY(-5px);
                box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
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
            
            @media (max-width: 1200px) {
                .toc, .toc-toggle {
                    display: none;
                }
            }

            /* 新增卡片悬浮效果 */
            .card {
                /* 现有样式保持不变... */
                transform-origin: center;
                transition: all 0.4s cubic-bezier(0.165, 0.84, 0.44, 1);
            }
            
            .card:hover {
                transform: translateY(-8px) scale(1.01);
                box-shadow: 0 15px 30px rgba(0, 0, 0, 0.15);
            }
            
            /* 标题样式优化 */
            .card h2 {
                position: relative;
                padding-left: 15px;
                margin-bottom: 25px;
                font-size: 1.6em;
                letter-spacing: 0.5px;
            }
            
            .card h2::before {
                content: '';
                position: absolute;
                left: 0;
                top: 0;
                height: 100%;
                width: 4px;
                background: var(--secondary-color);
                border-radius: 2px;
            }
            
            /* 链接样式美化 */
            .card a {
                position: relative;
                color: var(--secondary-color);
                text-decoration: none;
                padding-bottom: 2px;
            }
            
            .card a::after {
                content: '';
                position: absolute;
                bottom: 0;
                left: 0;
                width: 0;
                height: 1px;
                background: var(--secondary-color);
                transition: width 0.3s ease;
            }
            
            .card a:hover::after {
                width: 100%;
            }
            
            /* 列表样式优化 */
            .card ul {
                padding-left: 20px;
                list-style: none;
            }
            
            .card ul li {
                position: relative;
                padding: 8px 0;
                padding-left: 25px;
                line-height: 1.6;
            }
            
            .card ul li::before {
                content: '•';
                position: absolute;
                left: 0;
                color: var(--secondary-color);
                font-size: 1.2em;
                font-weight: bold;
            }
            
            /* 程序信息卡片美化 */
            .program-info {
                background: linear-gradient(145deg, 
                    rgba(255, 255, 255, 0.05) 0%, 
                    rgba(255, 255, 255, 0.1) 100%
                );
                border: 1px solid rgba(255, 255, 255, 0.1);
                backdrop-filter: blur(10px);
                -webkit-backdrop-filter: blur(10px);
            }
            
            .info-item {
                position: relative;
                overflow: hidden;
            }
            
            .info-item::before {
                content: '';
                position: absolute;
                top: -50%;
                left: -50%;
                width: 200%;
                height: 200%;
                background: radial-gradient(
                    circle,
                    rgba(255, 255, 255, 0.1) 0%,
                    transparent 70%
                );
                opacity: 0;
                transition: opacity 0.3s ease;
            }
            
            .info-item:hover::before {
                opacity: 1;
            }
            
            /* 滚动条美化 */
            ::-webkit-scrollbar {
                width: 8px;
                height: 8px;
            }
            
            ::-webkit-scrollbar-track {
                background: rgba(0, 0, 0, 0.1);
                border-radius: 4px;
            }
            
            ::-webkit-scrollbar-thumb {
                background: var(--secondary-color);
                border-radius: 4px;
            }
            
            ::-webkit-scrollbar-thumb:hover {
                background: #0052a3;
            }
            
            /* 页面加载动画 */
            @keyframes fadeInUp {
                from {
                    opacity: 0;
                    transform: translateY(20px);
                }
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }
            
            .content-section {
                animation: fadeInUp 0.8s ease-out;
            }
            
            /* 目录样式优化 */
            .toc {
                background: rgba(255, 255, 255, 0.1);
                backdrop-filter: blur(10px);
                -webkit-backdrop-filter: blur(10px);
                border: 1px solid rgba(255, 255, 255, 0.1);
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
            }
            
            .toc-item a {
                display: block;
                padding: 8px 12px;
                color: var(--primary-color);
                border-radius: 6px;
                transition: all 0.3s ease;
            }
            
            .toc-item a:hover {
                background: rgba(255, 255, 255, 0.1);
                transform: translateX(5px);
            }
            
            .toc-item.active a {
                background: var(--secondary-color);
                color: white;
            }
            
            /* 总结卡片特殊样式 */
            .summary-card {
                background: linear-gradient(145deg,
                    rgba(var(--secondary-color-rgb), 0.05) 0%,
                    rgba(var(--secondary-color-rgb), 0.1) 100%
                );
                border: 2px solid rgba(var(--secondary-color-rgb), 0.1);
            }
            
            .summary-card h2 {
                text-align: center;
                font-size: 2em;
                margin-bottom: 30px;
                color: var(--secondary-color);
                text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            }
            
            /* 响应式优化 */
            @media (max-width: 768px) {
                .card {
                    padding: 15px;
                }
                
                .card h2 {
                    font-size: 1.4em;
                }
                
                .toc {
                    display: none;
                }
                
                .program-info {
                    margin: 20px 10px;
                }
            }

            /* 标题样式美化 */
            h1, h2 {
                position: relative;
                padding: 15px 25px;
                margin: 0 0 25px 0;
                background: linear-gradient(135deg, rgba(0, 102, 204, 0.1), rgba(0, 82, 164, 0.05));
                border-radius: 10px;
                border-left: 5px solid var(--secondary-color);
                box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
                font-weight: 600;
                letter-spacing: 0.5px;
                transition: all 0.3s ease;
            }

            h1:hover, h2:hover {
                transform: translateX(5px);
                background: linear-gradient(135deg, rgba(0, 102, 204, 0.15), rgba(0, 82, 164, 0.1));
            }

            /* 特别为红框标记的标题添加样式 */
            .main-title {
                background: linear-gradient(135deg, rgba(255, 255, 255, 0.1), rgba(255, 255, 255, 0.05));
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 15px;
                padding: 20px;
                margin-bottom: 30px;
                backdrop-filter: blur(10px);
                -webkit-backdrop-filter: blur(10px);
                box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
                display: flex;
                align-items: center;
                gap: 10px;
            }

            .main-title h2 {
                margin: 0;
                padding: 0;
                border: none;
                background: none;
                box-shadow: none;
                color: var(--secondary-color);
                font-size: 1.8em;
            }

            .main-title:hover {
                transform: translateY(-3px);
                box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15);
            }

            /* 为emoji添加动画效果 */
            .main-title .emoji {
                font-size: 1.5em;
                display: inline-block;
                transition: transform 0.3s ease;
            }

            .main-title:hover .emoji {
                transform: scale(1.2) rotate(10deg);
            }
        </style>
        """

    @staticmethod
    def get_javascript():
        return """
        <script>
            document.addEventListener('DOMContentLoaded', function() {{
                // 暗色模式切换功能
                const darkModeToggle = document.getElementById('darkModeToggle');
                if (darkModeToggle) {{
                    darkModeToggle.addEventListener('click', function() {{
                        document.body.classList.toggle('dark-mode');
                        this.textContent = document.body.classList.contains('dark-mode') 
                            ? '切换到亮色模式' 
                            : '切换到暗色模式';
                    }});
                }}

                // 目录功能
                const tocToggle = document.querySelector('.toc-toggle');
                const toc = document.querySelector('.toc');
                
                if (tocToggle && toc) {{
                    tocToggle.addEventListener('click', function() {{
                        toc.classList.toggle('visible');
                    }});
                }}
                
                // 生成目录内容
                function generateToc() {{
                    const headings = document.querySelectorAll('.card h2');
                    const tocList = document.querySelector('.toc-list');
                    
                    if (!tocList) return;
                    
                    tocList.innerHTML = '';
                    
                    headings.forEach((heading, index) => {{
                        heading.id = `heading-${{index}}`;
                        
                        const li = document.createElement('li');
                        li.classList.add('toc-item');
                        
                        const a = document.createElement('a');
                        a.href = `#heading-${{index}}`;
                        a.textContent = heading.textContent;
                        a.addEventListener('click', function(e) {{
                            e.preventDefault();
                            heading.scrollIntoView({{ behavior: 'smooth' }});
                        }});
                        
                        li.appendChild(a);
                        tocList.appendChild(li);
                    }});
                }}
                
                // 更新目录激活状态
                function updateTocActiveState() {{
                    const headings = document.querySelectorAll('.card h2');
                    const tocItems = document.querySelectorAll('.toc-item');
                    
                    headings.forEach((heading, index) => {{
                        const rect = heading.getBoundingClientRect();
                        if (rect.top >= 0 && rect.top <= window.innerHeight * 0.5) {{
                            tocItems.forEach(item => item.classList.remove('active'));
                            tocItems[index].classList.add('active');
                        }}
                    }});
                }}
                
                generateToc();
                window.addEventListener('scroll', updateTocActiveState);
            }});

            // 平滑滚动
            document.querySelectorAll('a[href^="#"]').forEach(anchor => {{
                anchor.addEventListener('click', function (e) {{
                    e.preventDefault();
                    document.querySelector(this.getAttribute('href')).scrollIntoView({{
                        behavior: 'smooth'
                    }});
                }});
            }});
            
            // 添加淡入效果
            function addFadeInEffect() {{
                const cards = document.querySelectorAll('.card');
                const observer = new IntersectionObserver((entries) => {{
                    entries.forEach(entry => {{
                        if (entry.isIntersecting) {{
                            entry.target.classList.add('fade-in');
                            observer.unobserve(entry.target);
                        }}
                    }});
                }}, {{ threshold: 0.1 }});
                
                cards.forEach(card => observer.observe(card));
            }}
            
            window.addEventListener('load', addFadeInEffect);

            // 返回顶部功能和进度条
            const backToTop = document.querySelector('.back-to-top');
            window.addEventListener('scroll', () => {{
                if (window.scrollY > 300) {{
                    backToTop.classList.add('visible');
                }} else {{
                    backToTop.classList.remove('visible');
                }}
                
                const winScroll = document.body.scrollTop || document.documentElement.scrollTop;
                const height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
                const scrolled = (winScroll / height) * 100;
                document.querySelector('.progress-bar').style.width = scrolled + '%';
            }});

            // 返回顶部点击事件
            document.querySelector('.back-to-top').addEventListener('click', () => {{
                window.scrollTo({{
                    top: 0,
                    behavior: 'smooth'
                }});
            }});
        </script>
    """

    @staticmethod
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

    @staticmethod
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

    @staticmethod
    def generate_html_structure(content, generation_time):
        return f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <link rel="icon" type="image/png" href="../assets/favicon.png">
            <title>🎧Raddit_AI_search🎧</title>
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
            {HTMLGenerator.get_css()}
            {HTMLGenerator.get_shader()}
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
                <h1>🚀 Reddit AI 探索者 🤖</h1>
                <button id="darkModeToggle">切换到暗色模式</button>
            </header>
            <div class="container">
                <div class="main-title">
                    <span class="emoji">🌟</span>
                    <h2>AI's Wild West: The Latest Frontier in Tech-savvy Shenanigans</h2>
                    <span class="emoji">✨</span>
                </div>
                {content}
            </div>
            <footer>
                <p>生成于 {generation_time}</p>
            </footer>
            <div class="back-to-top">
                <i class="fas fa-arrow-up"></i>
            </div>
            <script>
                // 将所有功能包装在一个函数中
                function initializePage() {{
                    // 暗色模式切换功能
                    const darkModeToggle = document.getElementById('darkModeToggle');
                    if (darkModeToggle) {{
                        darkModeToggle.addEventListener('click', function() {{
                            document.body.classList.toggle('dark-mode');
                            this.textContent = document.body.classList.contains('dark-mode') 
                                ? '切换到亮色模式' 
                                : '切换到暗色模式';
                        }});
                    }}

                    // 目录功能
                    const tocToggle = document.querySelector('.toc-toggle');
                    const toc = document.querySelector('.toc');
                    
                    if (tocToggle && toc) {{
                        tocToggle.addEventListener('click', function() {{
                            toc.classList.toggle('visible');
                        }});
                    }}
                    
                    // 生成目录内容
                    function generateToc() {{
                        const headings = document.querySelectorAll('.card h2');
                        const tocList = document.querySelector('.toc-list');
                        
                        if (!tocList) return;
                        
                        tocList.innerHTML = '';
                        
                        headings.forEach((heading, index) => {{
                            heading.id = `heading-${{index}}`;
                            
                            const li = document.createElement('li');
                            li.classList.add('toc-item');
                            
                            const a = document.createElement('a');
                            a.href = `#heading-${{index}}`;
                            a.textContent = heading.textContent;
                            a.addEventListener('click', function(e) {{
                                e.preventDefault();
                                heading.scrollIntoView({{ behavior: 'smooth' }});
                            }});
                            
                            li.appendChild(a);
                            tocList.appendChild(li);
                        }});
                    }}
                    
                    // 更新目录激活状态
                    function updateTocActiveState() {{
                        const headings = document.querySelectorAll('.card h2');
                        const tocItems = document.querySelectorAll('.toc-item');
                        
                        headings.forEach((heading, index) => {{
                            const rect = heading.getBoundingClientRect();
                            if (rect.top >= 0 && rect.top <= window.innerHeight * 0.5) {{
                                tocItems.forEach(item => item.classList.remove('active'));
                                tocItems[index].classList.add('active');
                            }}
                        }});
                    }}
                    
                    generateToc();
                    window.addEventListener('scroll', updateTocActiveState);

                    // 返回顶部功能和进度条
                    const backToTop = document.querySelector('.back-to-top');
                    window.addEventListener('scroll', () => {{
                        if (window.scrollY > 300) {{
                            backToTop.classList.add('visible');
                        }} else {{
                            backToTop.classList.remove('visible');
                        }}
                        
                        const winScroll = document.body.scrollTop || document.documentElement.scrollTop;
                        const height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
                        const scrolled = (winScroll / height) * 100;
                        document.querySelector('.progress-bar').style.width = scrolled + '%';
                    }});

                    // 返回顶部点击事件
                    backToTop.addEventListener('click', () => {{
                        window.scrollTo({{
                            top: 0,
                            behavior: 'smooth'
                        }});
                    }});

                    // 添加淡入效果
                    const cards = document.querySelectorAll('.card');
                    const observer = new IntersectionObserver((entries) => {{
                        entries.forEach(entry => {{
                            if (entry.isIntersecting) {{
                                entry.target.classList.add('fade-in');
                                observer.unobserve(entry.target);
                            }}
                        }});
                    }}, {{ threshold: 0.1 }});
                    
                    cards.forEach(card => observer.observe(card));
                }}

                // 在 DOM 加载完成后初始化所有功能
                document.addEventListener('DOMContentLoaded', initializePage);
            </script>
            {HTMLGenerator.get_renderer_js()}
        </body>
        </html>
        """

def custom_markdown_to_html(md_content):
    # 分离主要内容和程序运行信息
    main_content, run_info = split_content(md_content)
    
    html_content = "<div class='container main-content'>"
    html_content += "<div class='content-section'>"  # 添加内容区域包装
    
    # 处理主要内容
    pattern = r'(## .+?\n)(.+?)(?=\n## |\n\nIn a world|\n\nAnd there you have it|\Z)'
    matches = re.findall(pattern, main_content, re.DOTALL)
    
    # 添加常规卡片
    for title, content in matches:
        if not any(keyword in title.lower() for keyword in ["总结", "summary", "conclusion"]):
            html_title = markdown2.markdown(title.strip())
            html_content += f"<div class='card'>{html_title}{markdown2.markdown(content.strip())}</div>"
    
    # 查找并添加总结部分 - 支持多种总结开头
    summary_pattern = r'\n\n(In a world.*?|And there you have it.*?)(?=\n*?-{3,}|\Z)'
    summary_match = re.search(summary_pattern, main_content, re.DOTALL)
    if summary_match:
        summary_content = summary_match.group(1).strip()
        html_content += f"""
        <div class='card summary-card'>
            <h2>Summary and Prospect 🚀</h2>
            {markdown2.markdown(summary_content)}
        </div>
        """
    
    html_content += "</div>"  # 结束内容区域
    
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
        # 提取主要内容（在运行信息之前的所有内容）
        main_content = md_content[:match.start()].strip()
        
        # 格式化运行信息HTML，调整时间显示格式
        run_info = f"""
            <div class='info-item'>
                <i class='fas fa-play-circle'></i>
                <span class='info-label'>开始时���</span>
                <span class='info-value'>{match.group(1).strip()}</span>
            </div>
            <div class='info-item'>
                <i class='fas fa-stop-circle'></i>
                <span class='info-label'>结束时间</span>
                <span class='info-value'>{match.group(2).strip()}</span>
            </div>
            <div class='info-item'>
                <i class='fas fa-clock'></i>
                <span class='info-label'>运行时长</span>
                <span class='info-value'>{match.group(3).strip()} 秒</span>
            </div>
            <div class='info-item'>
                <i class='fas fa-microchip'></i>
                <span class='info-label'>使用模型</span>
                <span class='info-value'>{match.group(4).strip()}</span>
            </div>
        """
    else:
        main_content = md_content
        run_info = ""
    
    return main_content, run_info

def generate_html(input_markdown_file, output_html_file):
    with open(input_markdown_file, "r", encoding="utf-8") as md_file:
        md_content = md_file.read()

    html_content = custom_markdown_to_html(md_content)

    html_structure = HTMLGenerator.generate_html_structure(html_content, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    with open(output_html_file, "w", encoding="utf-8") as html_file:
        html_file.write(html_structure)
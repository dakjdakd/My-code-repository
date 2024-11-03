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
                position: relative;
                z-index: 1;
                background: rgba(244, 244, 244, 0.9);
                border-radius: 15px;
                backdrop-filter: blur(10px);
                -webkit-backdrop-filter: blur(10px);
                margin: 20px auto;
                padding: 20px;
            }
            header {
                background-color: var(--secondary-color);
                color: white;
                text-align: center;
                padding: 1em;
                position: relative;
                z-index: 1;
                background: rgba(0, 102, 204, 0.9);
                backdrop-filter: blur(10px);
                -webkit-backdrop-filter: blur(10px);
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
                background: rgba(255, 255, 255, 0.9);
                backdrop-filter: blur(5px);
                -webkit-backdrop-filter: blur(5px);
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
                position: relative;
                z-index: 1;
                background: rgba(0, 102, 204, 0.9);
                backdrop-filter: blur(10px);
                -webkit-backdrop-filter: blur(10px);
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
            body.dark-mode .container {
                background: rgba(44, 44, 44, 0.9);
            }
            body.dark-mode .card {
                background: rgba(60, 60, 60, 0.9);
            }
            body.dark-mode header,
            body.dark-mode footer {
                background: rgba(26, 26, 26, 0.9);
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

    @staticmethod
    def get_javascript():
        return """
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
        #define T (time * 0.2)
        #define hue(a) (.6+.6*cos(6.3*(a)+vec3(0,83,21)))
        float rnd(float a) {
            vec2 p=fract(a*vec2(12.9898,78.233)); p+=dot(p,p*345.);
            return fract(p.x*p.y);
        }
        vec3 pattern(vec2 uv) {
            vec3 col=vec3(0);
            for (float i=.0; i++<20.;) {
                float a=rnd(i);
                vec2 n=vec2(a,fract(a*34.56)), p=sin(n*(T+7.)+T*.5);
                float d=dot(uv-p,uv-p);
                col+=.00125/d*hue(dot(uv,uv)+i*.125+T);
            }
            return col;
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
            <title>AI新闻摘要</title>
            {HTMLGenerator.get_css()}
            {HTMLGenerator.get_shader()}
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
            {content}
            <footer>
                <p>生成于 {generation_time}</p>
            </footer>
            {HTMLGenerator.get_javascript()}
            {HTMLGenerator.get_renderer_js()}
        </body>
        </html>
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

def generate_html(input_markdown_file, output_html_file):
    with open(input_markdown_file, "r", encoding="utf-8") as md_file:
        md_content = md_file.read()

    html_content = custom_markdown_to_html(md_content)

    html_structure = HTMLGenerator.generate_html_structure(html_content, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    with open(output_html_file, "w", encoding="utf-8") as html_file:
        html_file.write(html_structure)
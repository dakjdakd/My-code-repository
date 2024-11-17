class App {
    constructor() {
        // 初始化时确保脚本容器是隐藏的
        const scriptContainer = document.getElementById('scriptContainer');
        if (scriptContainer) {
            scriptContainer.classList.add('hidden');
            scriptContainer.innerHTML = ''; // 清空任何可能的内容
        }
        
        // 等待 DOM 加载完成后初始化
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => this.init());
        } else {
            this.init();
        }
    }

    init() {
        console.log('Initializing app...');
        this.setupEventListeners();
    }

    setupEventListeners() {
        // 直接获取元素
        const uploadBtn = document.getElementById('uploadBtn');
        const inputBtn = document.getElementById('inputBtn');
        const inputArea = document.getElementById('inputArea');
        const fileUploadArea = document.getElementById('fileUpload');
        const generateScript = document.getElementById('generateScript');

        console.log('Found elements:', {
            uploadBtn: !!uploadBtn,
            inputBtn: !!inputBtn,
            inputArea: !!inputArea,
            fileUploadArea: !!fileUploadArea,
            generateScript: !!generateScript
        });

        // 直接输入按钮事件
        if (inputBtn) {
            inputBtn.addEventListener('click', () => {
                console.log('Input button clicked');
                if (inputArea) {
                    inputArea.classList.remove('hidden');
                }
                if (fileUploadArea) {
                    fileUploadArea.classList.add('hidden');
                }
            });
        }

        // 上传文件按钮事件
        if (uploadBtn) {
            uploadBtn.addEventListener('click', () => {
                console.log('Upload button clicked');
                if (fileUploadArea) {
                    fileUploadArea.classList.remove('hidden');
                }
                if (inputArea) {
                    inputArea.classList.add('hidden');
                }
                
                // 创建文件上传区域
                fileUploadArea.innerHTML = `
                    <div class="file-upload-container">
                        <label class="file-upload-label">
                            <i data-lucide="upload-cloud" class="upload-icon"></i>
                            <span class="upload-text">点击或拖拽文件到这里上传</span>
                            <span class="upload-hint">支持 PDF、TXT 格式文件</span>
                            <div class="file-types">
                                <span class="file-type-tag">PDF</span>
                                <span class="file-type-tag">TXT</span>
                            </div>
                            <input type="file" 
                                   id="fileInput" 
                                   class="hidden" 
                                   accept=".txt,.pdf"
                                   aria-label="文件上传">
                        </label>
                    </div>
                `;
                
                // 初始化图标
                if (window.lucide) {
                    window.lucide.createIcons();
                }

                // 设置文件选择监听器
                const fileInput = document.getElementById('fileInput');
                if (fileInput) {
                    fileInput.addEventListener('change', (e) => this.handleFileUpload(e));
                }
            });
        }

        // 生成脚本按钮事件
        if (generateScript) {
            generateScript.addEventListener('click', async () => {
                console.log('Generate script button clicked');
                const contentInput = document.getElementById('contentInput');
                const content = contentInput?.value?.trim();
                
                if (!content) {
                    alert('请输入要转换的内容');
                    return;
                }

                await this.generatePodcast(content);
            });
        }
    }

    async handleFileUpload(event) {
        const file = event.target.files[0];
        if (!file) return;

        const formData = new FormData();
        formData.append('file', file);

        try {
            // 显示加载状态
            document.getElementById('loading')?.classList.remove('hidden');

            const response = await fetch('http://localhost:5000/api/upload', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                throw new Error('文件上传失败');
            }

            const result = await response.json();
            console.log('Upload Response:', result);
            await this.generatePodcast(result.content);

        } catch (error) {
            console.error('Upload Error:', error);
            alert('文件上传失败，请重试');
        } finally {
            document.getElementById('loading')?.classList.add('hidden');
        }
    }

    async generatePodcast(content) {
        try {
            // 显示加载状态
            const generateButton = document.getElementById('generateScript');
            const loaderContainer = document.querySelector('.loader-container');
            
            if (generateButton) generateButton.style.display = 'none';
            if (loaderContainer) loaderContainer.classList.remove('hidden');
            
            console.log("开始生成播客...");
            console.log("发送的内容:", content);
            
            const requestData = {
                content,
                host: document.getElementById('hostInput').value.trim() || '张斌',
                expert: document.getElementById('expertInput').value.trim() || '',
                dialogueLength: document.querySelector('input[name="dialogueLength"]:checked').value
            };
            
            console.log("请求数据:", requestData);

            const response = await fetch('http://localhost:5001/api/process', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                },
                body: JSON.stringify(requestData)
            });
            
            console.log("服务器响应状态:", response.status);

            if (!response.ok) {
                const errorData = await response.json();
                console.error("服务器错误:", errorData);
                throw new Error(errorData.error || '生成失败');
            }

            const result = await response.json();
            console.log('API Response:', result);
            
            if (result && result.script && result.script.length > 0) {
                this.displayResults(result);
            }

        } catch (error) {
            console.error('Error details:', error);
            console.error('Error stack:', error.stack);
            alert(`生成失败: ${error.message || '请检查后端服务是否正在运行'}`);
        } finally {
            // 恢复按钮状态
            const generateButton = document.getElementById('generateScript');
            const loaderContainer = document.querySelector('.loader-container');
            
            if (generateButton) generateButton.style.display = 'flex';
            if (loaderContainer) loaderContainer.classList.add('hidden');
        }
    }

    displayResults(result) {
        // 获取脚本容器
        const scriptContainer = document.getElementById('scriptContainer');
        if (!scriptContainer) return;
        
        // 只有在有内容时才显示容器
        if (result && result.script && result.script.length > 0) {
            // 清空原有内容
            scriptContainer.innerHTML = '';
            
            // 创建知识点容器（完全独立的容器）
            const knowledgeContainer = document.createElement('div');
            knowledgeContainer.className = 'knowledge-container';
            knowledgeContainer.innerHTML = `
                <h2 class="section-title">主要知识点</h2>
                <div class="knowledge-points-wrapper">
                    ${result.key_points.map(point => `
                        <div class="knowledge-point">
                            <span class="point-title">${point.title}</span>
                            <div class="point-subtopics">
                                ${point.subtopics.map(sub => `
                                    <span class="subtopic">${sub}</span>
                                `).join('')}
                            </div>
                        </div>
                    `).join('')}
                </div>
            `;
            
            // 创建对话内容容器（完全独立的容器）
            const dialogueContainer = document.createElement('div');
            dialogueContainer.className = 'dialogue-container';
            dialogueContainer.innerHTML = `
                <h2 class="section-title">对话内容</h2>
                <div class="dialogue-content">
                    ${result.script.map(segment => `
                        <div class="dialogue-segment ${segment.role} animate-fade-in">
                            <span class="role-label">
                                ${segment.role === 'interviewer' ? '主持人' : '专家'}
                            </span>
                            <p class="dialogue-text">${segment.content}</p>
                        </div>
                    `).join('')}
                </div>
            `;
            
            // 分别添加到页面
            const container = document.getElementById('scriptContainer');
            container.appendChild(knowledgeContainer);
            // 添加分隔空间
            const spacer = document.createElement('div');
            spacer.style.height = '3rem';  // 增加明显的间距
            container.appendChild(spacer);
            container.appendChild(dialogueContainer);
            
            // 最后才显示容器
            scriptContainer.classList.remove('hidden');
        } else {
            // 如果没有内容，确保容器是隐藏的
            scriptContainer.classList.add('hidden');
            scriptContainer.innerHTML = '';
        }
    }
}

// 创建应用实例
document.addEventListener('DOMContentLoaded', () => {
    console.log('Creating App instance...');
    window.app = new App();
});
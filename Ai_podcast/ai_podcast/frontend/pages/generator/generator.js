// 继承原有的 App 类功能
class PodcastGenerator {
    constructor() {
        this.apiBaseUrl = 'http://localhost:5001/api';
        this.init();
    }

    init() {
        // 确保 DOM 加载完成后再初始化
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => this.setupEventListeners());
        } else {
            this.setupEventListeners();
        }
    }

    setupEventListeners() {
        // 获取所有需要的元素
        const uploadBtn = document.getElementById('uploadBtn');
        const inputBtn = document.getElementById('inputBtn');
        const inputArea = document.getElementById('inputArea');
        const fileUploadArea = document.getElementById('fileUpload');
        const generateBtn = document.getElementById('generateScript');
        const contentInput = document.getElementById('contentInput');

        console.log('Elements found:', {
            uploadBtn: !!uploadBtn,
            inputBtn: !!inputBtn,
            inputArea: !!inputArea,
            fileUploadArea: !!fileUploadArea,
            generateBtn: !!generateBtn,
            contentInput: !!contentInput
        });

        if (!uploadBtn || !inputBtn) {
            console.error('Required buttons not found');
            return;
        }

        // 上传文档按钮事件
        uploadBtn.addEventListener('click', () => {
            console.log('Upload button clicked');
            uploadBtn.classList.add('active');
            inputBtn.classList.remove('active');
            if (fileUploadArea) fileUploadArea.classList.remove('hidden');
            if (inputArea) inputArea.classList.add('hidden');
            if (generateBtn) generateBtn.classList.remove('hidden');
        });

        // 直接输入按钮事件
        inputBtn.addEventListener('click', () => {
            console.log('Input button clicked');
            inputBtn.classList.add('active');
            uploadBtn.classList.remove('active');
            if (inputArea) inputArea.classList.remove('hidden');
            if (fileUploadArea) fileUploadArea.classList.add('hidden');
            if (generateBtn) generateBtn.classList.remove('hidden');
        });

        // 监听输入框内容变化
        if (contentInput) {
            contentInput.addEventListener('input', () => {
                if (generateBtn) {
                    generateBtn.classList.toggle('hidden', !contentInput.value.trim());
                }
            });
        }

        // 生成按钮事件
        if (generateBtn) {
            generateBtn.addEventListener('click', () => {
                const content = contentInput?.value.trim();
                if (content) {
                    this.generatePodcast(content);
                }
            });
        }
    }

    async generatePodcast(content) {
        try {
            console.log("开始生成播客...");
            const loadingEl = document.getElementById('loading');
            if (loadingEl) loadingEl.classList.remove('hidden');

            const requestData = {
                content,
                host: document.getElementById('hostInput')?.value.trim() || '张斌',
                expert: document.getElementById('expertInput')?.value.trim() || '',
                dialogueLength: document.querySelector('input[name="dialogueLength"]:checked')?.value || 'long'
            };

            console.log("发送请求数据:", requestData);

            const response = await fetch(`${this.apiBaseUrl}/process`, {
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
            console.log('服务器返回数据:', result);

            // 确保结果容器存在
            const scriptContainer = document.getElementById('scriptContainer');
            if (!scriptContainer) {
                console.error('Script container not found');
                throw new Error('页面元素未找到');
            }

            // 创建结果容器（如果不存在）
            let keyPointsContent = document.getElementById('keyPointsContent');
            let scriptContent = document.getElementById('scriptContent');

            if (!keyPointsContent) {
                console.log('Creating keyPointsContent container');
                keyPointsContent = document.createElement('div');
                keyPointsContent.id = 'keyPointsContent';
                scriptContainer.appendChild(keyPointsContent);
            }

            if (!scriptContent) {
                console.log('Creating scriptContent container');
                scriptContent = document.createElement('div');
                scriptContent.id = 'scriptContent';
                scriptContainer.appendChild(scriptContent);
            }

            // 显示结果
            this.displayResults(result);

        } catch (error) {
            console.error('生成失败:', error);
            alert(error.message || '生成失败，请重试');
        } finally {
            const loadingEl = document.getElementById('loading');
            if (loadingEl) loadingEl.classList.add('hidden');
        }
    }

    displayResults(result) {
        console.log("开始显示结果...");
        
        // 更新主持人和专家名字
        const hostName = document.getElementById('hostName');
        const expertName = document.getElementById('expertName');
        
        if (hostName) hostName.textContent = document.getElementById('hostInput')?.value.trim() || '张斌';
        if (expertName) expertName.textContent = document.getElementById('expertInput')?.value.trim() || result.meta?.expert || '专家';

        // 显示知识点
        const keyPointsContent = document.getElementById('keyPointsContent');
        if (keyPointsContent && result.key_points?.length > 0) {
            console.log("显示知识点...");
            keyPointsContent.innerHTML = result.key_points.map(point => `
                <div class="knowledge-point-card">
                    <h4 class="knowledge-point-title">
                        <i data-lucide="check-circle"></i>
                        ${point.title}
                    </h4>
                    <ul class="knowledge-point-list">
                        ${point.subtopics.map(subtopic => `
                            <li class="knowledge-point-item">${subtopic}</li>
                        `).join('')}
                    </ul>
                </div>
            `).join('');
            
            // 重新初始化图标
            lucide.createIcons();
        }

        // 显示对话脚本
        const scriptContent = document.getElementById('scriptContent');
        if (scriptContent && result.script?.length > 0) {
            console.log("显示对话脚本...");
            scriptContent.innerHTML = result.script.map(segment => `
                <div class="dialogue-segment ${segment.role}">
                    <span class="role-label">
                        ${segment.role === 'interviewer' ? '主持人' : '专家'}
                    </span>
                    <p class="dialogue-content">${segment.content}</p>
                </div>
            `).join('');
        }

        // 显示容器并滚动到可见区域
        const scriptContainer = document.getElementById('scriptContainer');
        if (scriptContainer) {
            console.log("显示结果容器...");
            scriptContainer.classList.remove('hidden');
            scriptContainer.scrollIntoView({ behavior: 'smooth' });
        }
    }
}

// 初始化生成器
document.addEventListener('DOMContentLoaded', () => {
    console.log('初始化播客生成器...');
    window.podcastGenerator = new PodcastGenerator();
}); 
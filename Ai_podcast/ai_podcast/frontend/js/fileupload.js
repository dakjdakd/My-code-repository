class FileUpload {
    constructor(onFileSelect) {
        this.onFileSelect = onFileSelect;
        this.container = document.getElementById('fileUpload');
        this.render();
        this.setupEventListeners();
    }

    render() {
        this.container.innerHTML = `
            <div class="file-upload-container">
                <label class="file-upload-label">
                    <i data-lucide="upload-cloud" class="upload-icon"></i>
                    <div class="upload-text">拖拽文件到这里</div>
                    <div class="upload-hint">或者</div>
                    <button class="custom-file-btn">
                        选择文件上传
                    </button>
                    <div class="file-types">
                        <span class="file-type-tag">PDF 文档</span>
                        <span class="file-type-tag">TXT 文本</span>
                    </div>
                    <input type="file" class="hidden" accept=".txt,.pdf">
                </label>
            </div>
        `;
        lucide.createIcons();
    }

    async readFileContent(file) {
        if (file.type === 'application/pdf') {
            return new Promise((resolve, reject) => {
                const reader = new FileReader();
                reader.onload = async (e) => {
                    try {
                        // 对于PDF文件，直接发送二进制数据到后端处理
                        resolve(e.target.result);
                    } catch (error) {
                        reject(error);
                    }
                };
                reader.onerror = reject;
                reader.readAsText(file);
            });
        } else {
            // 对于文本文件，直接读取内容
            return await file.text();
        }
    }

    setupEventListeners() {
        const input = this.container.querySelector('input');
        const label = this.container.querySelector('label');

        input.addEventListener('change', async (e) => {
            const file = e.target.files?.[0];
            if (file) {
                try {
                    const content = await this.readFileContent(file);
                    this.onFileSelect(content);
                } catch (error) {
                    console.error('Error reading file:', error);
                    alert('读取文件时发生错误，请重试。');
                }
            }
        });

        // 拖放功能
        label.addEventListener('dragover', (e) => {
            e.preventDefault();
            label.classList.add('bg-gray-100');
        });

        label.addEventListener('dragleave', () => {
            label.classList.remove('bg-gray-100');
        });

        label.addEventListener('drop', async (e) => {
            e.preventDefault();
            label.classList.remove('bg-gray-100');
            
            const file = e.dataTransfer?.files[0];
            if (file) {
                try {
                    const content = await this.readFileContent(file);
                    this.onFileSelect(content);
                } catch (error) {
                    console.error('Error reading file:', error);
                    alert('读取文件时发生错误，请重试。');
                }
            }
        });
    }
}
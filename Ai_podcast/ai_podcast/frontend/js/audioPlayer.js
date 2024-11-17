class AudioPlayer {
    constructor(script) {
        this.script = script;
        this.currentIndex = 0;
        this.isPlaying = false;
        this.audio = new Audio();
        
        this.element = this.createPlayerElement();
        this.setupEventListeners();
    }

    createPlayerElement() {
        const container = document.createElement('div');
        container.className = 'w-full max-w-md mx-auto bg-white rounded-xl shadow-md overflow-hidden';
        container.innerHTML = `
            <div class="p-8">
                <div class="flex justify-center space-x-4">
                    <button class="play-button p-3 rounded-full bg-indigo-600 text-white hover:bg-indigo-700 transition-colors">
                        <i data-lucide="play" class="w-6 h-6"></i>
                    </button>
                    <button class="reset-button p-3 rounded-full bg-gray-200 text-gray-700 hover:bg-gray-300 transition-colors">
                        <i data-lucide="rotate-ccw" class="w-6 h-6"></i>
                    </button>
                </div>
                <div class="mt-4">
                    <div class="progress-bar">
                        <div class="progress-bar-fill" style="width: 0%"></div>
                    </div>
                </div>
            </div>
        `;
        return container;
    }

    setupEventListeners() {
        const playButton = this.element.querySelector('.play-button');
        const resetButton = this.element.querySelector('.reset-button');

        playButton.addEventListener('click', () => this.togglePlay());
        resetButton.addEventListener('click', () => this.resetAudio());
    }

    async generateAudio(script) {
        try {
            console.log("开始生成完整播客音频...");
            
            const response = await fetch('http://localhost:5000/api/generate-audio', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ script: script })
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || '生成音频失败');
            }

            const blob = await response.blob();
            console.log("获取到音频数据:", blob.size, "bytes");
            return URL.createObjectURL(blob);
        } catch (error) {
            console.error('Error generating audio:', error);
            throw new Error('生成音频失败: ' + error.message);
        }
    }

    showLoading(show) {
        const playButton = this.element.querySelector('.play-button');
        if (show) {
            playButton.disabled = true;
            playButton.innerHTML = `
                <div class="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
            `;
        } else {
            playButton.disabled = false;
            this.updatePlayButton();
        }
    }

    showError(message) {
        let errorDiv = this.element.querySelector('.error-message');
        if (!errorDiv) {
            errorDiv = document.createElement('div');
            errorDiv.className = 'error-message text-red-500 text-sm mt-2 text-center';
            this.element.querySelector('.p-8').appendChild(errorDiv);
        }
        errorDiv.textContent = message;
        
        setTimeout(() => {
            errorDiv.textContent = '';
        }, 3000);
    }

    async playScript() {
        try {
            const response = await fetch('http://localhost:5000/api/generate-audio', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    script: this.script
                })
            });

            if (!response.ok) {
                throw new Error('生成音频失败');
            }

            const audioBlob = await response.blob();
            const audioUrl = URL.createObjectURL(audioBlob);
            this.audio.src = audioUrl;
            
            // 返回音频 Blob 对象以供保存
            return audioBlob;
        } catch (error) {
            console.error('播放脚本失败:', error);
            throw error;
        }
    }

    togglePlay() {
        if (this.isPlaying) {
            this.audio.pause();
            this.isPlaying = false;
        } else {
            this.isPlaying = true;
            this.playScript();
        }
        this.updatePlayButton();
    }

    resetAudio() {
        this.audio.pause();
        this.audio.currentTime = 0;
        this.isPlaying = false;
        this.currentIndex = 0;
        this.updatePlayButton();
        this.updateProgressBar();
    }

    updatePlayButton() {
        const playButton = this.element.querySelector('.play-button');
        playButton.innerHTML = `
            <i data-lucide="${this.isPlaying ? 'pause' : 'play'}" class="w-6 h-6"></i>
        `;
        lucide.createIcons();
    }

    updateProgressBar() {
        const progressBar = this.element.querySelector('.progress-bar-fill');
        const progress = (this.currentIndex / this.script.length) * 100;
        progressBar.style.width = `${progress}%`;
    }

    destroy() {
        this.audio.pause();
        URL.revokeObjectURL(this.audio.src);
    }
}
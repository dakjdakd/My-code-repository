class HelpCenterManager {
    constructor() {
        this.init();
    }

    init() {
        this.setupSearch();
        this.setupFAQ();
        this.setupFeedbackForm();
    }

    setupSearch() {
        const searchInput = document.getElementById('searchInput');
        if (searchInput) {
            searchInput.addEventListener('input', (e) => {
                const searchTerm = e.target.value.toLowerCase();
                this.filterContent(searchTerm);
            });
        }
    }

    filterContent(searchTerm) {
        const sections = document.querySelectorAll('.help-section');
        sections.forEach(section => {
            const content = section.textContent?.toLowerCase() || '';
            const isMatch = content.includes(searchTerm);
            section.style.display = isMatch || searchTerm === '' ? 'block' : 'none';
        });
    }

    setupFAQ() {
        const faqItems = document.querySelectorAll('.faq-item');
        faqItems.forEach(item => {
            const question = item.querySelector('.faq-question');
            question?.addEventListener('click', () => {
                const isActive = item.classList.contains('active');
                // 关闭其他打开的FAQ
                faqItems.forEach(otherItem => {
                    if (otherItem !== item) {
                        otherItem.classList.remove('active');
                    }
                });
                // 切换当前FAQ的状态
                item.classList.toggle('active', !isActive);
            });
        });
    }

    setupFeedbackForm() {
        const form = document.getElementById('feedbackForm');
        form?.addEventListener('submit', async (e) => {
            e.preventDefault();
            await this.handleFeedbackSubmit(e.target);
        });
    }

    async handleFeedbackSubmit(form) {
        try {
            const formData = new FormData(form);
            const response = await fetch('/api/feedback', {
                method: 'POST',
                body: JSON.stringify(Object.fromEntries(formData)),
                headers: {
                    'Content-Type': 'application/json'
                }
            });

            if (response.ok) {
                this.showNotification('反馈已提交，感谢您的建议！', 'success');
                form.reset();
            } else {
                throw new Error('提交失败');
            }
        } catch (error) {
            this.showNotification('提交失败，请稍后重试', 'error');
        }
    }

    showNotification(message, type) {
        const notification = document.createElement('div');
        notification.className = `notification ${type}`;
        notification.textContent = message;
        
        document.body.appendChild(notification);
        
        setTimeout(() => {
            notification.classList.add('fade-out');
            setTimeout(() => notification.remove(), 300);
        }, 3000);
    }
}

// 初始化帮助中心
new HelpCenterManager(); 
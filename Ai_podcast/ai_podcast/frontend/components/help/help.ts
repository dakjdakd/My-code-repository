class HelpCenter {
    constructor() {
        this.init();
    }

    private init(): void {
        this.setupSearch();
        this.setupFAQ();
        this.setupFeedbackForm();
    }

    private setupSearch(): void {
        const searchInput = document.getElementById('searchInput') as HTMLInputElement;
        if (searchInput) {
            searchInput.addEventListener('input', (e) => {
                const searchTerm = (e.target as HTMLInputElement).value.toLowerCase();
                this.filterContent(searchTerm);
            });
        }
    }

    private filterContent(searchTerm: string): void {
        const sections = document.querySelectorAll<HTMLElement>('.help-section');
        sections.forEach(section => {
            const content = section.textContent?.toLowerCase() || '';
            const isMatch = content.includes(searchTerm);
            section.style.display = isMatch || searchTerm === '' ? 'block' : 'none';
        });
    }

    private setupFAQ(): void {
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

    private setupFeedbackForm(): void {
        const form = document.getElementById('feedbackForm');
        form?.addEventListener('submit', async (e) => {
            e.preventDefault();
            await this.handleFeedbackSubmit(e.target as HTMLFormElement);
        });
    }

    private async handleFeedbackSubmit(form: HTMLFormElement): Promise<void> {
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

    private showNotification(message: string, type: 'success' | 'error'): void {
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
new HelpCenter(); 
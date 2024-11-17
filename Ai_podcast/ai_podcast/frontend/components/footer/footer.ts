class Footer {
    constructor() {
        this.init();
    }

    private init(): void {
        this.setupSocialLinks();
        this.setupNewsletterForm();
        // @ts-ignore
        window.lucide?.createIcons();
    }

    private setupSocialLinks(): void {
        const socialLinks = document.querySelectorAll('.social-link');
        socialLinks.forEach(link => {
            link.addEventListener('click', (e: Event) => {
                e.preventDefault();
                const href = (link as HTMLAnchorElement).href;
                if (href) {
                    window.open(href, '_blank');
                }
            });
        });
    }

    private setupNewsletterForm(): void {
        const form = document.querySelector('.newsletter-form');
        if (form) {
            form.addEventListener('submit', (e: Event) => {
                e.preventDefault();
                const emailInput = form.querySelector('input[type="email"]') as HTMLInputElement;
                if (emailInput && emailInput.value) {
                    this.subscribeToNewsletter(emailInput.value);
                }
            });
        }
    }

    private async subscribeToNewsletter(email: string): Promise<void> {
        try {
            const response = await fetch('/api/subscribe', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ email }),
            });

            if (response.ok) {
                this.showMessage('订阅成功！感谢您的关注。', 'success');
            } else {
                throw new Error('订阅失败');
            }
        } catch (error) {
            this.showMessage('订阅失败，请稍后重试。', 'error');
        }
    }

    private showMessage(message: string, type: 'success' | 'error'): void {
        const messageElement = document.createElement('div');
        messageElement.className = `message ${type}`;
        messageElement.textContent = message;
        
        document.body.appendChild(messageElement);
        
        setTimeout(() => {
            messageElement.remove();
        }, 3000);
    }
}

// 初始化页脚
new Footer(); 
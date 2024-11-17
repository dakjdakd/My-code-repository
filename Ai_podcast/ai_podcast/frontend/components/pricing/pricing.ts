class Pricing {
    private monthlyPrices: HTMLElement[];
    private yearlyPrices: HTMLElement[];
    private billingToggle: HTMLInputElement;

    constructor() {
        this.monthlyPrices = Array.from(document.querySelectorAll('.amount.monthly'));
        this.yearlyPrices = Array.from(document.querySelectorAll('.amount.yearly'));
        this.billingToggle = document.getElementById('billingToggle') as HTMLInputElement;
        
        this.init();
    }

    private init(): void {
        this.setupBillingToggle();
        this.setupPlanButtons();
        this.addScrollAnimation();
    }

    private setupBillingToggle(): void {
        this.billingToggle.addEventListener('change', () => {
            const isYearly = this.billingToggle.checked;
            this.updatePriceDisplay(isYearly);
            this.updatePeriodText(isYearly);
        });
    }

    private updatePriceDisplay(isYearly: boolean): void {
        this.monthlyPrices.forEach(price => {
            price.classList.toggle('hidden', isYearly);
        });
        
        this.yearlyPrices.forEach(price => {
            price.classList.toggle('hidden', !isYearly);
        });
    }

    private updatePeriodText(isYearly: boolean): void {
        const periodTexts = document.querySelectorAll('.period');
        periodTexts.forEach(text => {
            if (text.parentElement?.querySelector('.amount')?.textContent !== '定制') {
                text.textContent = isYearly ? '/年' : '/月';
            }
        });
    }

    private setupPlanButtons(): void {
        const buttons = document.querySelectorAll('.plan-button');
        buttons.forEach(button => {
            button.addEventListener('click', (e) => {
                const plan = (e.target as HTMLElement).classList[1];
                this.handlePlanSelection(plan);
            });
        });
    }

    private handlePlanSelection(plan: string): void {
        switch (plan) {
            case 'free':
                this.redirectToSignup();
                break;
            case 'popular':
                this.showUpgradeModal();
                break;
            case 'enterprise':
                this.showContactForm();
                break;
        }
    }

    private redirectToSignup(): void {
        window.location.href = '/signup';
    }

    private showUpgradeModal(): void {
        // 实现升级模态框逻辑
        console.log('Show upgrade modal');
    }

    private showContactForm(): void {
        // 实现联系表单逻辑
        console.log('Show contact form');
    }

    private addScrollAnimation(): void {
        const cards = document.querySelectorAll('.pricing-card');
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('fade-in');
                    observer.unobserve(entry.target);
                }
            });
        }, {
            threshold: 0.1
        });

        cards.forEach(card => {
            card.classList.add('animate-on-scroll');
            observer.observe(card);
        });
    }
}

// 初始化价格页面
new Pricing(); 
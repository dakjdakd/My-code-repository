interface AuthState {
    currentTab: 'login' | 'register';
    isVisible: boolean;
}

class Auth {
    private state: AuthState;
    private modal: HTMLElement;
    
    constructor() {
        this.state = {
            currentTab: 'login',
            isVisible: false
        };
        
        this.modal = document.getElementById('authModal') as HTMLElement;
        this.init();
    }
    
    private init(): void {
        this.setupEventListeners();
        this.setupFormValidation();
    }
    
    private setupEventListeners(): void {
        // 切换标签
        const tabs = document.querySelectorAll('.auth-tab');
        tabs.forEach(tab => {
            tab.addEventListener('click', () => {
                const tabName = tab.getAttribute('data-tab') as 'login' | 'register';
                this.switchTab(tabName);
            });
        });
        
        // 关闭按钮
        const closeBtn = this.modal.querySelector('.close-btn');
        closeBtn?.addEventListener('click', () => this.hide());
        
        // 点击背景关闭
        this.modal.addEventListener('click', (e) => {
            if (e.target === this.modal) {
                this.hide();
            }
        });
        
        // 表单提交
        const loginForm = document.getElementById('loginForm');
        const registerForm = document.getElementById('registerForm');
        
        loginForm?.addEventListener('submit', (e) => this.handleLogin(e));
        registerForm?.addEventListener('submit', (e) => this.handleRegister(e));
        
        // 社交登录
        const socialButtons = document.querySelectorAll('.social-btn');
        socialButtons.forEach(btn => {
            btn.addEventListener('click', () => {
                const provider = btn.classList[1];
                this.handleSocialLogin(provider);
            });
        });
    }
    
    private setupFormValidation(): void {
        const forms = document.querySelectorAll('.auth-form');
        forms.forEach(form => {
            const inputs = form.querySelectorAll('input');
            inputs.forEach(input => {
                input.addEventListener('input', () => {
                    this.validateInput(input);
                });
            });
        });
    }
    
    private validateInput(input: HTMLInputElement): void {
        const value = input.value.trim();
        const type = input.type;
        
        let isValid = true;
        let errorMessage = '';
        
        switch (type) {
            case 'email':
                const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
                isValid = emailRegex.test(value);
                errorMessage = '请输入有效的邮箱地址';
                break;
                
            case 'password':
                isValid = value.length >= 6;
                errorMessage = '密码长度至少为6位';
                break;
                
            case 'text':
                isValid = value.length >= 2;
                errorMessage = '用户名至少需要2个字符';
                break;
        }
        
        this.showInputError(input, isValid ? '' : errorMessage);
    }
    
    private showInputError(input: HTMLInputElement, message: string): void {
        const formGroup = input.closest('.form-group');
        let errorElement = formGroup?.querySelector('.error-message');
        
        if (message) {
            if (!errorElement) {
                errorElement = document.createElement('div');
                errorElement.className = 'error-message text-red-500 text-sm mt-1';
                formGroup?.appendChild(errorElement);
            }
            errorElement.textContent = message;
        } else {
            errorElement?.remove();
        }
    }
    
    private switchTab(tab: 'login' | 'register'): void {
        this.state.currentTab = tab;
        
        // 更新标签样式
        document.querySelectorAll('.auth-tab').forEach(t => {
            t.classList.toggle('active', t.getAttribute('data-tab') === tab);
        });
        
        // 更新表单显示
        document.querySelectorAll('.auth-form').forEach(form => {
            form.classList.toggle('active', form.id === `${tab}Form`);
        });
    }
    
    public show(): void {
        this.state.isVisible = true;
        this.modal.classList.add('active');
        document.body.style.overflow = 'hidden';
    }
    
    public hide(): void {
        this.state.isVisible = false;
        this.modal.classList.remove('active');
        document.body.style.overflow = '';
    }
    
    private async handleLogin(e: Event): Promise<void> {
        e.preventDefault();
        const form = e.target as HTMLFormElement;
        const formData = new FormData(form);
        
        try {
            const response = await fetch('/api/auth/login', {
                method: 'POST',
                body: JSON.stringify(Object.fromEntries(formData)),
                headers: {
                    'Content-Type': 'application/json'
                }
            });
            
            if (response.ok) {
                const data = await response.json();
                localStorage.setItem('auth_token', data.token);
                this.hide();
                window.location.reload();
            } else {
                throw new Error('登录失败');
            }
        } catch (error) {
            this.showError('登录失败，请检查您的账号密码');
        }
    }
    
    private async handleRegister(e: Event): Promise<void> {
        e.preventDefault();
        const form = e.target as HTMLFormElement;
        const formData = new FormData(form);
        
        try {
            const response = await fetch('/api/auth/register', {
                method: 'POST',
                body: JSON.stringify(Object.fromEntries(formData)),
                headers: {
                    'Content-Type': 'application/json'
                }
            });
            
            if (response.ok) {
                this.switchTab('login');
                this.showSuccess('注册成功，请登录');
            } else {
                throw new Error('注册失败');
            }
        } catch (error) {
            this.showError('注册失败，请稍后重试');
        }
    }
    
    private handleSocialLogin(provider: string): void {
        // 实现社交登录逻辑
        console.log(`Social login with ${provider}`);
    }
    
    private showError(message: string): void {
        // 显示错误提示
        const errorElement = document.createElement('div');
        errorElement.className = 'auth-error bg-red-100 text-red-700 p-3 rounded-lg mb-4';
        errorElement.textContent = message;
        
        const activeForm = document.querySelector('.auth-form.active');
        activeForm?.insertBefore(errorElement, activeForm.firstChild);
        
        setTimeout(() => errorElement.remove(), 3000);
    }
    
    private showSuccess(message: string): void {
        // 显示成功提示
        const successElement = document.createElement('div');
        successElement.className = 'auth-success bg-green-100 text-green-700 p-3 rounded-lg mb-4';
        successElement.textContent = message;
        
        const activeForm = document.querySelector('.auth-form.active');
        activeForm?.insertBefore(successElement, activeForm.firstChild);
        
        setTimeout(() => successElement.remove(), 3000);
    }
}

// 初始化认证组件
const auth = new Auth();
export default auth; 
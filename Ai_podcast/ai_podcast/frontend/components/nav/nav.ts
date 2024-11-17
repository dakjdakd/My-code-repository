interface NavState {
    isLoggedIn: boolean;
    currentPath: string;
}

class Navigation {
    private state: {
        isLoggedIn: boolean;
        currentPath: string;
    };
    
    constructor() {
        console.log('Navigation constructor called');
        this.state = {
            isLoggedIn: this.checkAuthStatus(),
            currentPath: window.location.pathname
        };
        
        this.init();
    }
    
    private init(): void {
        console.log('Navigation init called');
        // 立即设置按钮事件
        this.setupAuthButtons();
        this.highlightCurrentPage();
        
        // 监听导航内容变化
        const observer = new MutationObserver(() => {
            this.setupAuthButtons();
        });
        
        const navContainer = document.querySelector('.nav-container');
        if (navContainer) {
            observer.observe(navContainer, { 
                childList: true,
                subtree: true 
            });
        }
    }
    
    private setupAuthButtons(): void {
        console.log('Setting up auth buttons');
        
        // 获取按钮元素
        const loginBtn = document.querySelector('.login-btn') as HTMLButtonElement;
        const signupBtn = document.querySelector('.signup-btn') as HTMLButtonElement;
        
        console.log('Login button:', loginBtn);
        console.log('Signup button:', signupBtn);
        
        if (loginBtn) {
            loginBtn.onclick = (e: Event) => {
                e.preventDefault();
                e.stopPropagation();
                console.log('Login button clicked');
                // 使用绝对路径
                window.location.href = '/pages/auth/auth.html';
            };
        }
        
        if (signupBtn) {
            signupBtn.onclick = (e: Event) => {
                e.preventDefault();
                e.stopPropagation();
                console.log('Signup button clicked');
                // 使用绝对路径
                window.location.href = '/pages/auth/auth.html#register';
            };
        }
    }
    
    private showUserMenu(): void {
        const authContainer = document.querySelector('.nav-auth');
        if (authContainer) {
            authContainer.innerHTML = `
                <div class="user-menu">
                    <button class="user-menu-btn">
                        <i data-lucide="user" class="nav-icon"></i>
                        <span>我的账户</span>
                    </button>
                    <button class="logout-btn">
                        <i data-lucide="log-out" class="nav-icon"></i>
                        <span>退出登录</span>
                    </button>
                </div>
            `;
            
            // 重新初始化图标
            lucide.createIcons();
            
            // 设置退出登录按钮事件
            const logoutBtn = document.querySelector('.logout-btn');
            if (logoutBtn) {
                logoutBtn.addEventListener('click', () => this.handleLogout());
            }
        }
    }
    
    private highlightCurrentPage(): void {
        const links = document.querySelectorAll('.nav-link');
        links.forEach(link => {
            if ((link as HTMLAnchorElement).href === window.location.href) {
                link.classList.add('active');
            }
        });
    }
    
    private handleLogout(): void {
        localStorage.removeItem('auth_token');
        window.location.reload();
    }
    
    private checkAuthStatus(): boolean {
        return !!localStorage.getItem('auth_token');
    }
}

// 将 Navigation 类添加到全局作用域
(window as any).Navigation = Navigation;

// 自动初始化
document.addEventListener('DOMContentLoaded', () => {
    console.log('Initializing Navigation');
    new Navigation();
}); 
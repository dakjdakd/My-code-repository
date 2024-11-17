var Navigation = /** @class */ (function () {
    function Navigation() {
        console.log('Navigation constructor called');
        this.state = {
            isLoggedIn: this.checkAuthStatus(),
            currentPath: window.location.pathname
        };
        this.init();
    }
    Navigation.prototype.init = function () {
        console.log('Navigation init called');
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => {
                this.setupAuthButtons();
                this.highlightCurrentPage();
            });
        } else {
            this.setupAuthButtons();
            this.highlightCurrentPage();
        }
    };
    Navigation.prototype.setupAuthButtons = function () {
        console.log('Setting up auth buttons');
        var loginBtn = document.querySelector('.login-btn');
        var signupBtn = document.querySelector('.signup-btn');
        
        if (loginBtn) {
            loginBtn.addEventListener('click', function(e) {
                e.preventDefault();
                e.stopPropagation();
                console.log('Login button clicked');
                window.location.href = '/pages/auth/auth.html';
            });
        }
        
        if (signupBtn) {
            signupBtn.addEventListener('click', function(e) {
                e.preventDefault();
                e.stopPropagation();
                console.log('Signup button clicked');
                window.location.href = '/pages/auth/auth.html#register';
            });
        }
    };
    Navigation.prototype.showUserMenu = function () {
        var authContainer = document.querySelector('.nav-auth');
        if (authContainer) {
            authContainer.innerHTML = "\n                <div class=\"user-menu\">\n                    <button class=\"user-menu-btn\">\n                        <i data-lucide=\"user\" class=\"nav-icon\"></i>\n                        <span>\u6211\u7684\u8D26\u6237</span>\n                    </button>\n                    <button class=\"logout-btn\">\n                        <i data-lucide=\"log-out\" class=\"nav-icon\"></i>\n                        <span>\u9000\u51FA\u767B\u5F55</span>\n                    </button>\n                </div>\n            ";
            lucide.createIcons();
            var logoutBtn = document.querySelector('.logout-btn');
            if (logoutBtn) {
                logoutBtn.addEventListener('click', () => this.handleLogout());
            }
        }
    };
    Navigation.prototype.highlightCurrentPage = function () {
        var links = document.querySelectorAll('.nav-link');
        links.forEach(function (link) {
            if (link.href === window.location.href) {
                link.classList.add('active');
            }
        });
    };
    Navigation.prototype.handleLogout = function () {
        localStorage.removeItem('auth_token');
        window.location.reload();
    };
    Navigation.prototype.checkAuthStatus = function () {
        return !!localStorage.getItem('auth_token');
    };
    return Navigation;
}());

// 将 Navigation 类添加到全局作用域
window.Navigation = Navigation;

// 自动初始化
document.addEventListener('DOMContentLoaded', function () {
    console.log('Initializing Navigation');
    new Navigation();
});

// 监听导航内容变化
const observer = new MutationObserver(function(mutations) {
    mutations.forEach(function(mutation) {
        if (mutation.type === 'childList') {
            console.log('Navigation content changed, reinitializing buttons');
            new Navigation().setupAuthButtons();
        }
    });
});

// 开始观察导航容器
const navContainer = document.getElementById('nav-container');
if (navContainer) {
    observer.observe(navContainer, {
        childList: true,
        subtree: true
    });
} 
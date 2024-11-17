class Navigation {
    constructor() {
        this.init();
    }

    init() {
        this.loadNavigation();
    }

    loadNavigation() {
        const navHtml = `
            <nav class="nav-container">
                <div class="nav-wrapper">
                    <!-- 品牌标识 -->
                    <div class="nav-brand">
                        <a href="/ai_podcast/frontend/index.html" class="brand-link">AI播客生成器</a>
                    </div>

                    <!-- 主导航菜单 -->
                    <div class="nav-menu">
                        <a href="/ai_podcast/frontend/index.html" class="nav-link">
                            <i data-lucide="home" class="nav-icon"></i>
                            首页
                        </a>
                        <a href="/ai_podcast/frontend/pages/about/about.html" class="nav-link">
                            <i data-lucide="info" class="nav-icon"></i>
                            关于
                        </a>
                        <a href="/ai_podcast/frontend/pages/pricing/pricing.html" class="nav-link">
                            <i data-lucide="tag" class="nav-icon"></i>
                            价格
                        </a>
                        <a href="/ai_podcast/frontend/pages/help/help.html" class="nav-link">
                            <i data-lucide="help-circle" class="nav-icon"></i>
                            帮助
                        </a>
                    </div>

                    <!-- 用户操作区 -->
                    <div class="nav-auth">
                        <a href="/ai_podcast/frontend/pages/user/profile.html" class="profile-btn">
                            <i data-lucide="user" class="nav-icon"></i>
                            个人中心
                        </a>
                        <button class="login-btn">登录</button>
                        <button class="signup-btn">注册</button>
                    </div>
                </div>
            </nav>
        `;

        const navContainer = document.getElementById('nav-container');
        if (navContainer) {
            navContainer.innerHTML = navHtml;
            this.highlightCurrentPage();
            lucide.createIcons();
        }
    }

    highlightCurrentPage() {
        const currentPath = window.location.pathname;
        const links = document.querySelectorAll('.nav-link, .brand-link, .profile-btn');
        
        links.forEach(link => {
            const href = link.getAttribute('href');
            if (href && currentPath.endsWith(href)) {
                link.classList.add('active');
            } else {
                link.classList.remove('active');
            }
        });
    }
}

// 初始化导航
new Navigation(); 
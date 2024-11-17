class Router {
    constructor() {
        this.routes = {
            '/': '/index.html',
            '/about': '/pages/about/about.html',
            '/pricing': '/pages/pricing/pricing.html',
            '/help': '/pages/help/help.html',
            '/user/profile': '/pages/user/profile.html'
        };
        
        this.init();
    }

    init() {
        // 拦截所有导航链接的点击
        document.addEventListener('click', (e) => {
            const link = e.target.closest('a');
            if (link && link.href && !link.hasAttribute('download')) {
                const url = new URL(link.href);
                
                // 只处理同域名下的链接
                if (url.origin === window.location.origin) {
                    e.preventDefault();
                    this.navigate(url.pathname);
                }
            }
        });

        // 处理浏览器前进后退
        window.addEventListener('popstate', () => {
            this.handleRoute(window.location.pathname);
        });

        // 处理初始路由
        if (window.location.pathname !== '/') {
            this.handleRoute(window.location.pathname);
        }
    }

    async handleRoute(pathname) {
        try {
            // 如果是首页，不需要加载内容
            if (pathname === '/') {
                return;
            }

            const route = this.routes[pathname];
            if (!route) {
                throw new Error('Page not found');
            }

            // 获取页面内容
            const response = await fetch(route);
            if (!response.ok) throw new Error('Failed to load page');
            
            const html = await response.text();
            
            // 提取 body 内容
            const parser = new DOMParser();
            const doc = parser.parseFromString(html, 'text/html');
            const content = doc.querySelector('body').innerHTML;
            
            // 更新页面内容
            document.getElementById('app').innerHTML = content;
            
            // 重新初始化图标
            lucide.createIcons();
            
            // 更新标题
            const title = doc.querySelector('title');
            if (title) {
                document.title = title.textContent;
            }
            
            // 滚动到顶部
            window.scrollTo(0, 0);
            
        } catch (error) {
            console.error('路由错误:', error);
            document.getElementById('app').innerHTML = `
                <div class="container mx-auto px-4 py-12">
                    <h1 class="text-2xl text-white">页面未找到</h1>
                </div>
            `;
        }
    }

    navigate(path) {
        window.history.pushState({}, '', path);
        this.handleRoute(path);
    }
}

// 等待 DOM 加载完成后初始化路由
document.addEventListener('DOMContentLoaded', () => {
    window.router = new Router();
}); 
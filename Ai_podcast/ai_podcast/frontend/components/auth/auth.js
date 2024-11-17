console.log('Auth.js loaded');

document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM Content Loaded in auth.js');
    
    // 获取所有DOM元素
    const loginForm = document.getElementById('loginForm');
    const registerForm = document.getElementById('registerForm');
    const authTabs = document.querySelectorAll('.auth-tab');
    const welcomeText = document.querySelector('.welcome-text');
    
    // 调试日志
    console.log('Forms found:', {
        loginForm: loginForm,
        registerForm: registerForm,
        authTabs: authTabs,
        welcomeText: welcomeText
    });
    
    // 切换表单显示
    function switchForm(targetForm) {
        console.log('Switching to form:', targetForm);
        
        // 更新欢迎文本
        if (welcomeText) {
            welcomeText.textContent = targetForm === 'login' 
                ? '欢迎回来，请登录您的账号' 
                : '创建新账号，开启AI播客之旅';
        }
        
        // 更新表单显示状态
        if (loginForm && registerForm) {
            if (targetForm === 'login') {
                loginForm.classList.remove('hidden');
                registerForm.classList.add('hidden');
                loginForm.classList.add('active');
                registerForm.classList.remove('active');
            } else {
                loginForm.classList.add('hidden');
                registerForm.classList.remove('hidden');
                loginForm.classList.remove('active');
                registerForm.classList.add('active');
            }
        }
        
        // 更新标签状态
        authTabs.forEach(tab => {
            const isActive = tab.getAttribute('data-tab') === targetForm;
            tab.classList.toggle('active', isActive);
        });
    }
    
    // 绑定标签点击事件
    authTabs.forEach(tab => {
        tab.addEventListener('click', () => {
            const targetForm = tab.getAttribute('data-tab');
            console.log('Tab clicked:', targetForm);
            switchForm(targetForm);
        });
    });
    
    // 处理 URL hash
    function handleHash() {
        const hash = window.location.hash.slice(1);
        console.log('Handling hash:', hash);
        if (hash === 'register') {
            switchForm('register');
        }
    }
    
    // 初始化时处理 hash
    handleHash();
    
    // 监听 hash 变化
    window.addEventListener('hashchange', handleHash);
    
    // 登录表单处理
    if (loginForm) {
        loginForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const email = document.getElementById('loginEmail').value;
            const password = document.getElementById('loginPassword').value;
            const remember = document.querySelector('input[name="remember"]')?.checked;
            
            try {
                const response = await fetch('/api/auth/login', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ email, password, remember }),
                });
                
                const data = await response.json();
                
                if (response.ok) {
                    localStorage.setItem('auth_token', data.token);
                    window.location.href = '/';
                } else {
                    showError(data.error || '登录失败', 'loginForm');
                }
            } catch (error) {
                console.error('登录错误:', error);
                showError('网络错误，请稍后重试', 'loginForm');
            }
        });
    }
    
    // 注册表单处理
    if (registerForm) {
        registerForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const email = document.getElementById('registerEmail').value;
            const password = document.getElementById('registerPassword').value;
            const confirmPassword = document.getElementById('confirmPassword').value;
            
            if (!email || !password || !confirmPassword) {
                showError('请填写所有必填字段', 'registerForm');
                return;
            }
            
            if (password !== confirmPassword) {
                showError('两次输入的密码不一致', 'registerForm');
                return;
            }
            
            try {
                const response = await fetch('/api/auth/register', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ 
                        email, 
                        password,
                        username: email.split('@')[0] // 临时使用邮箱前缀作为用户名
                    }),
                });
                
                const data = await response.json();
                
                if (response.ok) {
                    // 注册成功后切换到登录表单
                    switchForm('login');
                    showSuccess('注册成功，请登录');
                } else {
                    showError(data.error || '注册失败', 'registerForm');
                }
            } catch (error) {
                console.error('注册错误:', error);
                showError('网络错误，请稍后重试', 'registerForm');
            }
        });
    }
    
    // 错误提示函数
    function showError(message, formId) {
        const form = document.getElementById(formId);
        let errorDiv = form.querySelector('.error-message');
        
        if (!errorDiv) {
            errorDiv = document.createElement('div');
            errorDiv.className = 'error-message text-red-500 text-sm mt-2';
            form.appendChild(errorDiv);
        }
        
        errorDiv.textContent = message;
        setTimeout(() => {
            errorDiv.textContent = '';
        }, 3000);
    }
    
    // 成功提示函数
    function showSuccess(message) {
        const successDiv = document.createElement('div');
        successDiv.className = 'success-message text-green-500 text-sm mt-2';
        successDiv.textContent = message;
        
        const container = document.querySelector('.auth-container');
        container.appendChild(successDiv);
        
        setTimeout(() => {
            successDiv.remove();
        }, 3000);
    }
}); 
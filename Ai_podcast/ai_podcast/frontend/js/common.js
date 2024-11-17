// 加载背景组件
function loadBackground() {
    // 检查是否已存在背景组件
    if (!document.querySelector('.gradient-bg')) {
        // 创建背景HTML
        const backgroundHTML = `
            <div class="gradient-bg">
                <div class="gradients-container">
                    <div class="g1"></div>
                    <div class="g2"></div>
                    <div class="g3"></div>
                    <div class="g4"></div>
                    <div class="g5"></div>
                </div>
            </div>
        `;
        
        // 确保 SVG 滤镜存在
        if (!document.querySelector('filter#goo')) {
            const svgFilter = `
                <svg class="hidden">
                    <filter id="goo">
                        <feGaussianBlur in="SourceGraphic" stdDeviation="10" result="blur" />
                        <feColorMatrix in="blur" mode="matrix" values="1 0 0 0 0  0 1 0 0 0  0 0 1 0 0  0 0 0 18 -8" result="goo" />
                        <feBlend in="SourceGraphic" in2="goo" />
                    </filter>
                </svg>
            `;
            document.body.insertAdjacentHTML('afterbegin', svgFilter);
        }
        
        // 插入背景HTML
        document.body.insertAdjacentHTML('afterbegin', backgroundHTML);
    }
    
    // 无论是否新创建背景，都要初始化渐变效果
    if (typeof initGradients === 'function') {
        initGradients();
    }
}

// 确保在页面加载完成后初始化背景
document.addEventListener('DOMContentLoaded', () => {
    loadBackground();
});

// 确保在页面完全加载后也初始化背景
window.addEventListener('load', () => {
    loadBackground();
    // 额外调用一次初始化，确保渐变效果正确显示
    if (typeof initGradients === 'function') {
        setTimeout(initGradients, 100);
    }
}); 
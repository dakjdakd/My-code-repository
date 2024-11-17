function initGradients() {
    const gradients = document.querySelectorAll('.g1, .g2, .g3, .g4, .g5');
    
    gradients.forEach((gradient, index) => {
        // 随机初始位置
        const x = Math.random() * 100 - 50;
        const y = Math.random() * 100 - 50;
        const scale = 0.8 + Math.random() * 0.4;
        
        // 设置初始位置和大小
        gradient.style.transform = `translate(${x}%, ${y}%) scale(${scale})`;
        gradient.style.animationDelay = `-${Math.random() * 50}s`;
        
        // 渐现效果
        gradient.style.opacity = '0';
        gradient.style.transition = 'opacity 1s ease-in';
        
        setTimeout(() => {
            gradient.style.opacity = '0.7';
        }, index * 200);
    });
}

// 页面可见性变化时重新初始化
document.addEventListener('visibilitychange', () => {
    if (!document.hidden) {
        initGradients();
    }
});

// 每隔一段时间重新初始化一次位置
setInterval(initGradients, 60000);
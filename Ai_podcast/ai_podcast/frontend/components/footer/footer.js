// 加载页脚内容
fetch('/components/footer/footer.html')
    .then(response => response.text())
    .then(html => {
        document.getElementById('footer-container').innerHTML = html;
        // 重新初始化图标
        lucide.createIcons();
    }); 
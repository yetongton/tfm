// 在页面加载完成后执行
document.addEventListener('DOMContentLoaded', function() {
    // 设置警告消息自动消失
    const alerts = document.querySelectorAll('.alert:not(.alert-no-dismiss)');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            const closeButton = alert.querySelector('.btn-close');
            if (closeButton) {
                closeButton.click();
            }
        }, 5000); // 5秒后自动消失
    });

    // 确认密码验证
    const registerForm = document.querySelector('form[action*="/register"]');
    if (registerForm) {
        registerForm.addEventListener('submit', function(e) {
            const password = document.getElementById('password').value;
            const confirmPassword = document.getElementById('confirm_password').value;
            
            if (password !== confirmPassword) {
                e.preventDefault();
                alert('两次输入的密码不一致！');
            }
        });
    }

    // 表格排序功能
    document.querySelectorAll('th[data-sort]').forEach(function(th) {
        th.addEventListener('click', function() {
            const table = th.closest('table');
            const tbody = table.querySelector('tbody');
            const rows = Array.from(tbody.querySelectorAll('tr'));
            const index = Array.from(th.parentNode.children).indexOf(th);
            const direction = th.dataset.direction === 'asc' ? 'desc' : 'asc';
            
            // 重置所有表头的排序方向
            th.parentNode.querySelectorAll('th').forEach(function(el) {
                el.dataset.direction = '';
                el.classList.remove('sorting-asc', 'sorting-desc');
            });
            
            // 设置当前表头的排序方向
            th.dataset.direction = direction;
            th.classList.add(direction === 'asc' ? 'sorting-asc' : 'sorting-desc');
            
            // 排序行
            rows.sort(function(a, b) {
                const aValue = a.children[index].textContent.trim();
                const bValue = b.children[index].textContent.trim();
                
                // 如果是数字，按数字排序
                if (!isNaN(aValue) && !isNaN(bValue)) {
                    return direction === 'asc' ? 
                        parseFloat(aValue) - parseFloat(bValue) : 
                        parseFloat(bValue) - parseFloat(aValue);
                }
                
                // 否则按文本排序
                return direction === 'asc' ? 
                    aValue.localeCompare(bValue) : 
                    bValue.localeCompare(aValue);
            });
            
            // 重新添加排序后的行
            rows.forEach(function(row) {
                tbody.appendChild(row);
            });
        });
    });

    // 表格搜索功能
    const tableSearchInputs = document.querySelectorAll('.table-search-input');
    tableSearchInputs.forEach(function(input) {
        input.addEventListener('keyup', function() {
            const searchText = this.value.toLowerCase();
            const table = document.querySelector(this.dataset.tableTarget);
            
            if (!table) return;
            
            const rows = table.querySelectorAll('tbody tr');
            
            rows.forEach(function(row) {
                const text = row.textContent.toLowerCase();
                if (text.includes(searchText)) {
                    row.style.display = '';
                } else {
                    row.style.display = 'none';
                }
            });
        });
    });

    // 添加平滑滚动效果
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;
            
            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                targetElement.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });

    // 为卡片添加鼠标悬停效果
    const cards = document.querySelectorAll('.card');
    cards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.classList.add('card-hover');
        });
        card.addEventListener('mouseleave', function() {
            this.classList.remove('card-hover');
        });
    });

    // 初始化工具提示
    if (typeof bootstrap !== 'undefined' && bootstrap.Tooltip) {
        const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }

    // 清除缓存的函数
    function clearBrowserCache() {
        // 添加时间戳到所有CSS和JS文件链接
        const links = document.querySelectorAll('link[rel="stylesheet"]');
        links.forEach(link => {
            if (link.href) {
                link.href = appendTimeStamp(link.href);
            }
        });
        
        const scripts = document.querySelectorAll('script[src]');
        scripts.forEach(script => {
            if (script.src) {
                script.src = appendTimeStamp(script.src);
            }
        });
    }
    
    // 添加时间戳的函数
    function appendTimeStamp(url) {
        const timestamp = new Date().getTime();
        const joiner = url.indexOf('?') !== -1 ? '&' : '?';
        return `${url}${joiner}_=${timestamp}`;
    }
    
    // 添加语言切换事件监听器
    const langLinks = document.querySelectorAll('.lang-switch');
    langLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            // 强制刷新页面
            sessionStorage.setItem('forceReload', 'true');
        });
    });
    
    // 检查是否需要强制刷新
    if (sessionStorage.getItem('forceReload') === 'true') {
        sessionStorage.removeItem('forceReload');
        clearBrowserCache();
        location.reload(true);
    }
}); 
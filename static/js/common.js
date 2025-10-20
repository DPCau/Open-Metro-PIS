// 公共JavaScript文件

// 更新时间函数
function updateTime() {
    const now = new Date();
    let hours = now.getHours().toString().padStart(2, '0');
    let minutes = now.getMinutes().toString().padStart(2, '0');
    let timeString = `${hours}:${minutes}`;
    
    const timeElements = document.querySelectorAll('.time');
    timeElements.forEach(el => {
        el.textContent = timeString;
    });
}

// 初始更新时间并设置定时器
window.addEventListener('load', () => {
    updateTime();
    setInterval(updateTime, 60000); // 每分钟更新一次
});

// 获取线路颜色
function getLineColor(lineName) {
    const lineColors = {
        'line_1': '#ff6b6b',
        'line_2': '#4ecdc4',
        'line_3': '#ffe66d',
        'line_4': '#1a535c',
        'line_5': '#9b5de5',
        'line_6': '#f15bb5',
        'line_7': '#fee440',
        'line_8': '#00bbf9',
        'line_9': '#00f5d4'
    };
    
    return lineColors[lineName] || '#6c757d';
}

// 获取线路名称显示
function getLineDisplayName(lineName) {
    const lineNames = {
        'line_1': '1号线',
        'line_2': '2号线',
        'line_3': '3号线',
        'line_4': '4号线',
        'line_5': '5号线',
        'line_6': '6号线',
        'line_7': '7号线',
        'line_8': '8号线',
        'line_9': '9号线'
    };
    
    return lineNames[lineName] || lineName;
}

// 模拟数据请求函数
async function fetchData(endpoint, params = {}) {
    try {
        const queryParams = new URLSearchParams(params).toString();
        const url = `${endpoint}${queryParams ? '?' + queryParams : ''}`;
        const response = await fetch(url);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error('数据请求失败:', error);
        return { status: 'error', message: error.message };
    }
}

// 动画效果函数
function fadeIn(element, duration = 500) {
    element.style.opacity = '0';
    element.style.transition = `opacity ${duration}ms ease-in`;
    
    setTimeout(() => {
        element.style.opacity = '1';
    }, 10);
}

function slideIn(element, direction = 'left', duration = 500) {
    let initialTransform = 'translateX(-100%)';
    if (direction === 'right') initialTransform = 'translateX(100%)';
    if (direction === 'top') initialTransform = 'translateY(-100%)';
    if (direction === 'bottom') initialTransform = 'translateY(100%)';
    
    element.style.transform = initialTransform;
    element.style.transition = `transform ${duration}ms ease-out`;
    element.style.opacity = '1';
    
    setTimeout(() => {
        element.style.transform = 'translateX(0)';
    }, 10);
}

// 错误处理函数
function handleError(error, elementId = null) {
    console.error(error);
    
    if (elementId) {
        const element = document.getElementById(elementId);
        if (element) {
            element.innerHTML = `<div class="error-message">错误: ${error.message || error}</div>`;
        }
    }
}

// 页面跳转函数
function navigateTo(page) {
    window.location.href = page;
}

// 格式化站点索引信息
function formatStationIndex(index) {
    if (!Array.isArray(index) || index.length === 0) return '无数据';
    
    return index.map(item => {
        if (Array.isArray(item) && item.length >= 2) {
            return `${item[0]}行 ${item[1]}号`;
        }
        return String(item);
    }).join(', ');
}

// 防抖函数
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// 节流函数
function throttle(func, limit) {
    let inThrottle;
    return function() {
        const args = arguments;
        const context = this;
        if (!inThrottle) {
            func.apply(context, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}
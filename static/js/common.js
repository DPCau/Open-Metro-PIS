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
document.addEventListener('DOMContentLoaded', () => {
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

// 键盘快捷键监听
document.addEventListener('keydown', function(event) {
    // 1 -> 首页, 2 -> 线路图, 3 -> 线路详情
    if (event.key === '1') {
        navigateTo('/');
    } else if (event.key === '2') {
        navigateTo('/line_map');
    } else if (event.key === '3') {
        navigateTo('/line_detail');
    } else if (event.key === '4') {
            navigateTo('/arrival');
        } else if (event.key.toLowerCase() === 't') {
            // T 键 -> 切换开门侧
            fetch('/api/state/door/toggle', { method: 'POST' })
                .then(response => response.json())
                .then(data => {
                    if (data.status === 'success') {
                        window.location.reload();
                    }
                });
        } else if (event.key.toLowerCase() === 'f') {
            // F 键 -> 切换到下一站（不刷新）
            fetch('/api/state/next_no_refresh', { method: 'POST' })
                .then(response => response.json())
                .then(data => {
                    if (data.status === 'success') {
                        console.log('Next station updated to:', data.next_station);
                    }
                });
        } else if (event.key.toLowerCase() === 'd') {
        // D 键 -> 下一站
        fetch('/api/state/next', { method: 'POST' })
            .then(response => response.json())
            .then(data => {
                console.log('已切换至下一站:', data.next_station);
                window.location.reload(); // 刷新页面以更新显示
            })
            .catch(err => console.error('切换下一站失败:', err));
    } else if (event.key.toLowerCase() === 'a') {
        // A 键 -> 上一站
        fetch('/api/state/prev', { method: 'POST' })
            .then(response => response.json())
            .then(data => {
                console.log('已切换至上一站:', data.next_station);
                window.location.reload(); // 刷新页面以更新显示
            })
            .catch(err => console.error('切换上一站失败:', err));
    } else if (event.key.toLowerCase() === 'r') {
        // R 键 -> 一键反向
        fetch('/api/state/reverse', { method: 'POST' })
            .then(response => response.json())
            .then(data => {
                console.log('已切换方向:', data.direction === 0 ? '正向' : '反向');
                window.location.reload();
            })
            .catch(err => console.error('切换方向失败:', err));
    } else if (event.key.toLowerCase() === 's') {
        // S 键 -> 切换下一个路由
        fetch('/api/state/route/next', { method: 'POST' })
            .then(response => response.json())
            .then(data => {
                console.log('已切换路由:', data.route_name);
                window.location.reload();
            })
            .catch(err => console.error('切换路由失败:', err));
    } else if (event.key.toLowerCase() === 'w') {
        // W 键 -> 切换上一个路由
        fetch('/api/state/route/prev', { method: 'POST' })
            .then(response => response.json())
            .then(data => {
                console.log('已切换路由:', data.route_name);
                window.location.reload();
            })
            .catch(err => console.error('切换路由失败:', err));
    } else if (event.key.toLowerCase() === 'l') {
        // L 键 -> 切换下一条线路
        fetch('/api/state/line/next', { method: 'POST' })
            .then(response => response.json())
            .then(data => {
                console.log('已切换至线路:', data.line_name);
                window.location.reload();
            })
            .catch(err => console.error('切换线路失败:', err));
    } else if (event.key.toLowerCase() === 'k') {
        // K 键 -> 切换上一条线路
        fetch('/api/state/line/prev', { method: 'POST' })
            .then(response => response.json())
            .then(data => {
                console.log('已切换至线路:', data.line_name);
                window.location.reload();
            })
            .catch(err => console.error('切换线路失败:', err));
    } else if (event.key.toLowerCase() === 'i') {
        // i 键 -> 单行模式 (仅在页面2/线路图生效)
        if (window.location.pathname === '/line_map') {
            updateLayout('one_line');
        } else if (window.location.pathname === '/') {
            updateRunStyle('default');
        } else if (window.location.pathname === '/line_detail') {
            updateDetailStyle('default');
        }
    } else if (event.key.toLowerCase() === 'o') {
        // o 键 -> 双行模式 (仅在页面2/线路图生效)
        if (window.location.pathname === '/line_map') {
            updateLayout('two_line');
        } else if (window.location.pathname === '/') {
            // 检查是否存在分支
            const hasBranchesEl = document.getElementById('has-branches');
            const hasBranches = hasBranchesEl && hasBranchesEl.getAttribute('data-value') === 'true';
            
            if (hasBranches) {
                // 如果有分支，按o强制使用default模式
                updateRunStyle('default');
            } else {
                updateRunStyle('detail');
            }
        } else if (window.location.pathname === '/line_detail') {
            updateDetailStyle('column');
        }
    } else if (event.key.toLowerCase() === 'p') {
        // p 键 -> 自动模式 (仅在页面2/线路图生效)
        if (window.location.pathname === '/line_map') {
            updateLayout('auto');
        }
    }
});

// 更新布局模式
function updateLayout(mode) {
    fetch('/api/state/layout', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ mode: mode })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            console.log('布局模式已更新为:', data.layout);
            window.location.reload();
        } else {
            console.error('更新布局失败:', data.message);
        }
    })
    .catch(err => console.error('请求更新布局失败:', err));
}

function updateDetailStyle(style) {
    fetch('/api/state/detail_style', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ style: style })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            window.location.reload();
        } else {
            console.error('更新详情样式失败:', data.message);
        }
    })
    .catch(err => console.error('请求更新详情样式失败:', err));
}

function updateRunStyle(style) {
    fetch('/api/state/run_style', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ style: style })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            window.location.reload();
        } else {
            console.error('更新首页样式失败:', data.message);
        }
    })
    .catch(err => console.error('请求更新首页样式失败:', err));
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

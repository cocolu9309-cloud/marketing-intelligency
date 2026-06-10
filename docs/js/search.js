// 全局变量
let allArticles = [];
let currentFilters = {
    department: "all",
    contentType: "all",
    importance: "all",
    timeRange: "all",
    keyword: "",
    source: "all"
};

/**
 * 从 /data/articles.json 获取数据
 */
async function loadArticles() {
    try {
        const response = await fetch('../data/articles.json');
        if (!response.ok) throw new Error('Failed to load articles');
        allArticles = await response.json();
        updateLastUpdated();
        renderArticles();
    } catch (error) {
        console.error('加载文章失败:', error);
        document.getElementById('articlesContainer').innerHTML =
            '<div class="empty-state">加载失败，请刷新页面重试</div>';
    }
}

/**
 * 从最新文章获取时间，格式化为中文显示
 */
function updateLastUpdated() {
    if (!allArticles || allArticles.length === 0) return;
    const crawledAt = allArticles[0].crawled_at;
    const date = parseDate(crawledAt);
    const options = {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    };
    const formatted = date.toLocaleString('zh-CN', options);
    document.getElementById('lastUpdated').textContent = `最后更新: ${formatted}`;
}

/**
 * 解析 RFC 3339 日期字符串为 Date 对象
 */
function parseDate(dateStr) {
    return new Date(dateStr);
}

/**
 * 核心筛选函数
 */
function filterArticles() {
    return allArticles.filter(article => {
        // 部门筛选
        if (currentFilters.department !== 'all') {
            if (article.department !== currentFilters.department) return false;
        }

        // 内容类型筛选
        if (currentFilters.contentType !== 'all') {
            if (article.content_type !== currentFilters.contentType) return false;
        }

        // 重要程度筛选
        if (currentFilters.importance !== 'all') {
            if (article.importance !== currentFilters.importance) return false;
        }

        // 时间范围筛选
        if (currentFilters.timeRange !== 'all') {
            const articleDate = parseDate(article.published || article.crawled_at);
            const now = new Date();
            const diffMs = now - articleDate;
            const diffDays = diffMs / (1000 * 60 * 60 * 24);

            if (currentFilters.timeRange === 'today' && diffDays >= 1) return false;
            if (currentFilters.timeRange === 'week' && diffDays > 7) return false;
            if (currentFilters.timeRange === 'month' && diffDays > 30) return false;
        }

        // 关键词搜索
        if (currentFilters.keyword) {
            const keyword = currentFilters.keyword.toLowerCase();
            const searchableText = [
                article.title,
                article.one_sentence_summary || '',
                article.why_important || '',
                article.how_to_use || ''
            ].join(' ').toLowerCase();
            if (!searchableText.includes(keyword)) return false;
        }

        return true;
    });
}

/**
 * 渲染文章列表
 */
function renderArticles() {
    const filtered = filterArticles();
    const container = document.getElementById('articlesContainer');

    if (filtered.length === 0) {
        container.innerHTML = '<div class="empty-state">暂无符合条件的资讯</div>';
        return;
    }

    const html = filtered.map(article => {
        // 重要性星级（高=5星，中=3星，低=1星）
        const impMap = { "高": 5, "中": 3, "低": 1 };
        const stars = '★'.repeat(impMap[article.importance] || 3) + '☆'.repeat(5 - (impMap[article.importance] || 3));
        const date = parseDate(article.crawled_at).toLocaleString('zh-CN', {
            year: 'numeric',
            month: 'long',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        });
        // 中文标题优先显示
        const displayTitle = article.title_cn || article.title;

        return `
        <div class="article-card">
            <div class="article-header">
                <span class="importance-stars">${stars}</span>
                <h3 class="article-title">
                    <a href="${article.url}" target="_blank">${displayTitle}</a>
                </h3>
            </div>
            ${article.title_cn ? `<div class="article-original-title">原文: ${article.title}</div>` : ''}
            <div class="article-meta">
                <span class="tag department-tag">${article.department}</span>
                <span class="tag type-tag">${article.content_type}</span>
                <span class="tag source-tag">${article.source}</span>
                <span class="tag time-tag">${date}</span>
            </div>
            <div class="article-summary">
                <p class="one-sentence"><strong>一句话:</strong> ${article.one_sentence || '暂无'}</p>
                <p class="why-important"><strong>为什么重要:</strong> ${article.why_important || '暂无'}</p>
                <p class="how-to-use"><strong>怎么用:</strong> ${article.how_to_use || '暂无'}</p>
            </div>
            <div class="article-footer">
                <a href="${article.url}" target="_blank" class="btn-read-more">查看原文</a>
            </div>
        </div>
    `;
    }).join('');

    container.innerHTML = html;
}

/**
 * 初始化事件监听
 */
function initEventListeners() {
    // Tab 按钮点击
    document.querySelectorAll('.tab').forEach(tab => {
        tab.addEventListener('click', () => {
            document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
            tab.classList.add('active');
            currentFilters.department = tab.dataset.department || 'all';
            renderArticles();
        });
    });

    // 内容类型筛选
    document.getElementById('typeFilter').addEventListener('change', (e) => {
        currentFilters.contentType = e.target.value;
        renderArticles();
    });

    // 重要程度筛选
    document.getElementById('importanceFilter').addEventListener('change', (e) => {
        currentFilters.importance = e.target.value;
        renderArticles();
    });

    // 时间范围筛选
    document.getElementById('timeFilter').addEventListener('change', (e) => {
        currentFilters.timeRange = e.target.value;
        renderArticles();
    });

    // 搜索输入 - 300ms 防抖
    let searchTimeout;
    document.getElementById('searchInput').addEventListener('input', (e) => {
        clearTimeout(searchTimeout);
        searchTimeout = setTimeout(() => {
            currentFilters.keyword = e.target.value.trim();
            renderArticles();
        }, 300);
    });

    // 搜索按钮点击
    document.getElementById('searchBtn').addEventListener('click', () => {
        currentFilters.keyword = document.getElementById('searchInput').value.trim();
        renderArticles();
    });
}

// DOMContentLoaded 初始化
document.addEventListener('DOMContentLoaded', () => {
    initEventListeners();
    loadArticles();
});
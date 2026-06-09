// 全局变量
let allArticles = [];
let currentFilters = {
    department: 'all',
    contentType: 'all',
    importance: 'all',
    timeRange: 'all',
    keyword: ''
};

async function loadArticles() {
    try {
        const response = await fetch('./data/articles.json');
        if (!response.ok) throw new Error('Failed to load articles');
        allArticles = await response.json();
        updateLastUpdated();
        renderArticles();
    } catch (error) {
        document.getElementById('articlesContainer').innerHTML = '<div class="empty-state">加载失败</div>';
    }
}

function updateLastUpdated() {
    if (!allArticles || allArticles.length === 0) return;
    const date = new Date(allArticles[0].crawled_at);
    document.getElementById('lastUpdated').textContent = '最后更新: ' + date.toLocaleString('zh-CN');
}

function parseDate(dateStr) { return new Date(dateStr); }

function filterArticles() {
    return allArticles.filter(article => {
        if (currentFilters.department !== 'all' && article.department !== currentFilters.department) return false;
        if (currentFilters.contentType !== 'all' && article.content_type !== currentFilters.contentType) return false;
        if (currentFilters.importance !== 'all' && article.importance !== currentFilters.importance) return false;
        if (currentFilters.timeRange !== 'all') {
            const diffDays = (new Date() - parseDate(article.crawled_at)) / 86400000;
            if (currentFilters.timeRange === 'today' && diffDays > 1) return false;
            if (currentFilters.timeRange === 'week' && diffDays > 7) return false;
            if (currentFilters.timeRange === 'month' && diffDays > 30) return false;
        }
        if (currentFilters.keyword) {
            const text = (article.title + ' ' + (article['one_sentence']||'') + ' ' + (article['why_important']||'') + ' ' + (article['how_to_use']||'')).toLowerCase();
            if (!text.includes(currentFilters.keyword.toLowerCase())) return false;
        }
        return true;
    });
}

function renderArticles() {
    const filtered = filterArticles();
    const container = document.getElementById('articlesContainer');
    if (filtered.length === 0) { container.innerHTML = '<div class="empty-state">暂无符合条件的资讯</div>'; return; }
    container.innerHTML = filtered.map(function(article) {
        const date = parseDate(article.published || article.crawled_at).toLocaleDateString('zh-CN');
        return '<div class="article-card">' +
            '<div class="article-header"><span class="article-importance">' + article.importance + '</span>' +
            '<h3 class="article-title"><a href="' + article.url + '" target="_blank">' + article.title + '</a></h3></div>' +
            '<div class="article-meta"><span class="tag dept">' + article.department + '</span><span class="tag">' + article.content_type + '</span><span class="tag">' + (article.source_name || article.source) + '</span><span class="tag">' + date + '</span></div>' +
            '<div class="article-summary"><p><strong>📌 一句话：</strong>' + (article['one_sentence'] || '-') + '</p><p><strong>💡 为什么重要：</strong>' + (article['why_important'] || '-') + '</p><p><strong>🎯 怎么用：</strong>' + (article['how_to_use'] || '-') + '</p></div>' +
            '<div class="article-footer"><a class="article-link" href="' + article.url + '" target="_blank">查看原文 →</a></div>' +
        '</div>';
    }).join('');
}

function initEventListeners() {
    document.querySelectorAll('.tab').forEach(function(tab) {
        tab.addEventListener('click', function() {
            document.querySelectorAll('.tab').forEach(function(t) { t.classList.remove('active'); });
            tab.classList.add('active');
            currentFilters.department = tab.dataset.dept || 'all';
            renderArticles();
        });
    });
    document.getElementById('typeFilter').addEventListener('change', function(e) { currentFilters.contentType = e.target.value; renderArticles(); });
    document.getElementById('importanceFilter').addEventListener('change', function(e) { currentFilters.importance = e.target.value; renderArticles(); });
    document.getElementById('timeFilter').addEventListener('change', function(e) { currentFilters.timeRange = e.target.value; renderArticles(); });
    var timeout;
    document.getElementById('searchInput').addEventListener('input', function(e) { clearTimeout(timeout); timeout = setTimeout(function() { currentFilters.keyword = e.target.value.trim(); renderArticles(); }, 300); });
    document.getElementById('searchBtn').addEventListener('click', function() { currentFilters.keyword = document.getElementById('searchInput').value.trim(); renderArticles(); });
}

document.addEventListener('DOMContentLoaded', function() { initEventListeners(); loadArticles(); });
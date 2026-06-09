let allArticles = [];
let currentFilters = { department: 'all', contentType: 'all', importance: 'all', timeRange: 'all', keyword: '' };

async function loadArticles() {
    try {
        const resp = await fetch('./data/articles.json');
        if (!resp.ok) throw new Error('Failed');
        allArticles = await resp.json();
        updateLastUpdated();
        renderArticles();
    } catch (e) {
        document.getElementById('articlesContainer').innerHTML = '<p class=\"loading\">加载失败</p>';
    }
}

function updateLastUpdated() {
    if (!allArticles.length) return;
    document.getElementById('lastUpdated').textContent = new Date(allArticles[0].crawled_at).toLocaleString('zh-CN');
}

function parseDate(s) { return new Date(s); }

function filterArticles() {
    return allArticles.filter(a => {
        if (currentFilters.department !== 'all' && a.department !== currentFilters.department) return false;
        if (currentFilters.contentType !== 'all' && a.content_type !== currentFilters.contentType) return false;
        if (currentFilters.importance !== 'all' && a.importance !== currentFilters.importance) return false;
        if (currentFilters.timeRange !== 'all') {
            const d = parseDate(a.crawled_at);
            const now = new Date();
            const diff = (now - d) / 86400000;
            if (currentFilters.timeRange === 'today' && diff > 1) return false;
            if (currentFilters.timeRange === 'week' && diff > 7) return false;
            if (currentFilters.timeRange === 'month' && diff > 30) return false;
        }
        if (currentFilters.keyword) {
            const kw = currentFilters.keyword.toLowerCase();
            const t = (a.title+' '+(a.one_sentence||'')+' '+(a.why_important||'')+' '+(a.how_to_use||'')).toLowerCase();
            if (!t.includes(kw)) return false;
        }
        return true;
    });
}

function renderArticles() {
    const f = filterArticles();
    const c = document.getElementById('articlesContainer');
    if (!f.length) { c.innerHTML = '<p class=\"loading\">暂无符合条件的资讯</p>'; return; }
    c.innerHTML = f.map(a => {
        const d = parseDate(a.published || a.crawled_at).toLocaleDateString('zh-CN');
        return '<div class=\"article-card\">'+
            '<div class=\"article-header\"><span class=\"article-importance\">'+a.importance+'</span>'+
            '<div class=\"article-title-wrap\"><h3 class=\"article-title\"><a href=\"'+a.url+'\" target=\"_blank\">'+a.title+'</a></h3><p class=\"article-title-cn\">'+a.title+'</p></div></div>'+
            '<div class=\"article-meta\"><span class=\"tag dept\">'+a.department+'</span><span class=\"tag\">'+a.content_type+'</span><span class=\"tag\">来源:'+(a.source_name||a.source)+'</span><span class=\"tag\">'+d+'</span></div>'+
            '<div class=\"article-summary\"><p><strong>📌 一句话：</strong>'+(a.one_sentence||'-')+'</p><p><strong>💡 为什么重要：</strong>'+(a.why_important||'-')+'</p><p><strong>🎯 怎么用：</strong>'+(a.how_to_use||'-')+'</p></div>'+
            '<div class=\"article-footer\"><a class=\"article-link\" href=\"'+a.url+'\" target=\"_blank\">查看原文 →</a></div></div>';
    }).join('');
}

function initEventListeners() {
    document.querySelectorAll('.tab').forEach(t => t.addEventListener('click', function() {
        document.querySelectorAll('.tab').forEach(x => x.classList.remove('active'));
        this.classList.add('active');
        currentFilters.department = this.dataset.dept || 'all';
        renderArticles();
    }));
    document.getElementById('typeFilter').addEventListener('change', e => { currentFilters.contentType = e.target.value; renderArticles(); });
    document.getElementById('importanceFilter').addEventListener('change', e => { currentFilters.importance = e.target.value; renderArticles(); });
    document.getElementById('timeFilter').addEventListener('change', e => { currentFilters.timeRange = e.target.value; renderArticles(); });
    let tm;
    document.getElementById('searchInput').addEventListener('input', e => { clearTimeout(tm); tm = setTimeout(() => { currentFilters.keyword = e.target.value.trim(); renderArticles(); }, 300); });
    document.getElementById('searchBtn').addEventListener('click', () => { currentFilters.keyword = document.getElementById('searchInput').value.trim(); renderArticles(); });
}
document.addEventListener('DOMContentLoaded', () => { initEventListeners(); loadArticles(); });

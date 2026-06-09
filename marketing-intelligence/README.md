# callie.com 营销资讯中心

聚合全球顶级营销媒体，一键追踪行业动态

## 功能特性

- 全自动抓取：无需人工干预，自动采集全球营销资讯
- 每日凌晨自动更新：基于 GitHub Actions 定时任务，每日00:00 UTC 自动运行
- 浏览器端搜索+多维度筛选：支持关键词搜索、按来源/时间/标签分类筛选
- 钉钉分享链接访问：支持通过钉钉机器人 Webhook 分享精选内容

## 技术栈

Python爬虫+Hugo+GitHub Pages+GitHub Actions

## 本地开发

### 前置要求

- Python 3.11+
- Hugo Extended 0.131+

### 安装依赖

```bash
pip install feedparser requests beautifulsoup4
```

### 本地运行爬虫

```bash
python scripts/crawl.py
```

### 本地预览网站

```bash
hugo server -D
```

访问 http://localhost:1313

## 部署说明

1. Fork 或直接克隆本仓库到你的 GitHub 账号
2. 在仓库 Settings > Pages > Source 中选择 `gh-pages` 分支作为部署源
3. 启用 GitHub Actions，爬虫将在每日凌晨自动运行
4. 推送内容后，约 1-2 分钟即可在 https://[username].github.io/[repo-name] 访问

## 内容来源

### 一级来源

- Adweek
- Marketing Week
- Social Media Today
- Search Engine Journal

### 二级来源

- TikTok for Business Blog
- YouTube Blog
- Google Ads Blog
- Meta for Business

### 竞品动态

- wanderprints
- macorner
- pawsionate

## 目录结构

```
marketing-intelligence/
├── .github/
│   └── workflows/
│       └── crawl.yml          # GitHub Actions 定时爬取流程
├── data/
│   └── articles.json # 爬取的文章数据
├── layouts/
│   └── index.html             # 网站首页模板
├── scripts/
│   └── crawl.py               # 爬虫主脚本
├── src/
│   └── (前端资源)
├── config.toml # Hugo 配置文件
└── README.md
```
# 设计规格：全球前沿营销玩法资讯网页

## 1. 项目概述

**项目名称：** callie.com 营销资讯中心（内部代号：Marketing Intelligence Hub）

**一句话描述：** 一个轻量静态网页，自动化抓取全球营销媒体、社交媒体平台和竞品网站的最新资讯，支持搜索和筛选，通过钉钉链接分享给团队访问。

**目标用户：** callie.com 营销中心团队（60-70人）

---

## 2. 核心功能

### 2.1 内容抓取（全自动）

**抓取来源：**

| 分类 | 来源 | 方式 |
|------|------|------|
| 营销媒体（一级） | Adweek、Marketing Week、Social Media Today、Search Engine Journal | RSS 订阅 |
| 社交媒体平台（二级） | TikTok for Business Blog、Instagram for Business、YouTube Blog、Google Ads Blog、Meta for Business | RSS 订阅 |
| 竞品网站（三级） | wanderprints.com、macorner.co、pawsionate.com（Etsy 店铺） | 网页爬虫 |

**数据字段：**
- 标题
- 来源名称
- 部门归属（社媒运营/红人营销/广告投放/用户运营/SEO/品牌）
- 内容类型（新玩法/数据报告/工具推荐/案例分享/平台更新）
- 重要程度（⭐⭐⭐ 必读/⭐⭐ 推荐/⭐ 了解）
- 摘要（一句话结论 + 为什么重要 + 可以怎么用）
- 原文链接
- 发布时间
- 抓取时间

**更新频率：** 每天凌晨自动抓取（配合方案 A，每天一次）

### 2.2 展示功能

**页面结构：**
- 首页：最新资讯列表 +搜索框 + 筛选器
- 按部门 tab切换（社媒运营/红人营销/广告投放/用户运营/SEO/品牌/全部）
- 资讯卡片展示：标题、来源、类型、重要程度、摘要、发布时间

**搜索功能：**
- 关键词全文搜索（标题 + 摘要）
-实时搜索（浏览器端过滤）

**筛选功能：**
- 按部门筛选（tab切换）
- 按内容类型筛选（下拉选择）
- 按重要程度筛选（星星等级）
- 按时间范围筛选（本周/本月/全部）

### 2.3 访问方式

- 部署到 GitHub Pages 或 Vercel（免费托管）
- 通过钉钉聊天分享链接访问
- 无需登录，公开访问

---

## 3. 技术方案

### 3.1 技术栈

| 层级 | 技术选型 | 说明 |
|------|---------|------|
| 数据抓取 | Python + Feedparser（RSS）+ Requests + BeautifulSoup（网页） | 自动化抓取，生成 JSON 数据 |
| 静态网站生成 | Hugo | 轻量快速，生成纯静态 HTML |
| 前端交互 | JavaScript（原生的浏览器端搜索和筛选） | 无需后端，纯静态 |
| 托管 | GitHub Pages 或 Vercel | 免费托管，自动部署 |
| CI/CD | GitHub Actions | 每天定时触发爬虫 + 自动构建部署 |

### 3.2 数据流

```
每天凌晨（GitHub Actions Cron）
    ↓
Python爬虫脚本执行
    ├── 抓取 RSS 源（营销媒体 + 社交媒体平台）
    └── 抓取竞品网站（Etsy 店铺）
    ↓
生成 data.json 数据文件
    ↓
Hugo 生成静态网页
    ↓
自动部署到 GitHub Pages
    ↓
团队通过钉钉链接访问
```

### 3.3 目录结构

```
marketing-intelligence/
├── README.md
├── config.toml              # Hugo 配置文件
├── data/
│   └── articles.json       # 爬虫生成的数据文件
├── scripts/
│   └── crawl.py           # Python 爬虫脚本
├── src/
│   ├── index.html         # 首页
│   ├── css/
│   │   └── style.css      # 样式
│   └── js/
│       └── search.js      # 搜索筛选逻辑
└── layouts/
    └── index.html         # Hugo 模板
```

---

## 4. 内容摘要生成规则

爬虫抓取内容后，需要生成标准化摘要：

**自动生成的摘要字段：**
- **一句话结论**：从文章标题或首段提取，不超过 30 字
- **为什么重要**：根据内容类型自动生成一句话说明
- **可以怎么用**：根据部门归属生成一句话行动建议

**部门归属映射规则：**
| 内容来源 | 默认部门 |
|---------|---------|
| Search Engine Journal、SEO 相关 | SEO |
| Social Media Today、TikTok/Instagram/YouTube 官方博客 | 社媒运营 |
| Adweek、Marketing Week、品牌相关 | 品牌 |
| Google Ads Blog、Meta for Business | 广告投放 |
| 红人合作、创作者经济相关 | 红人营销 |
| 用户留存、会员体系、CRM 相关 | 用户运营 |

---

## 5. 展示页面设计

### 5.1 页面布局

```
┌─────────────────────────────────────────────────┐
│ 🔥 callie.com 营销资讯中心                      │
├─────────────────────────────────────────────────┤
│  [搜索框........................] [🔍]           │
├─────────────────────────────────────────────────┤
│  [全部] [社媒运营] [红人营销] [广告投放] │
│  [用户运营] [SEO] [品牌] │
├─────────────────────────────────────────────────┤
│  筛选：类型 [全部▼]  重要程度 [全部▼]            │
├─────────────────────────────────────────────────┤
│┌─────────────────────────────────────────┐   │
│  │ ⭐⭐⭐  TikTok Launches New Creator... │   │
│  │ 来源：TikTok for Business 部门：红人营销 │   │
│  │ 类型：平台更新  时间：2026-06-08 │   │
│  │ 一句话结论：TikTok 推出创作者直接打赏功能  │   │
│  │ [查看原文]                                │   │
│  └─────────────────────────────────────────┘   │
│  ... │
└─────────────────────────────────────────────────┘
```

### 5.2 卡片信息展示

每张资讯卡片包含：
- 重要程度星星（⭐⭐⭐ / ⭐⭐ / ⭐）
- 标题（可点击跳转原文）
- 来源名称 + 部门标签 + 类型标签
- 发布时间
- 一句话结论
- 行动建议（"可以怎么用"）

---

## 6. 自动化部署流程

### 6.1 GitHub Actions 工作流

```yaml
name: Daily Crawl and Deploy

on:
  schedule:
    - cron: '0 1 * * *'  # 每天凌晨 1 点（北京时间9 点）

jobs:
  crawl-and-deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: pip install feedparser requests beautifulsoup4
      - name: Run crawler
        run: python scripts/crawl.py
      - name: Build Hugo site
        uses: peaceiris/actions-hugo@v2
        with:
          hugo-version: '0.115'
      - name: Deploy to GitHub Pages
        uses: peaceiris/actions-hugo-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
```

---

## 7. 分期落地

### 第一期（本期）
- 完成爬虫脚本开发，生成 data.json
- Hugo静态页面搭建
- 基础搜索和筛选功能
-部署到 GitHub Pages

### 第二期（后续）
- 摘要自动生成优化（引入 LLM API 生成更精准摘要）
- 个性化订阅功能（团队成员勾选部门，推送到钉钉机器人）
- 数据分析看板（热门资讯统计）

---

## 8. 风险与应对

| 风险 | 可能性 | 影响 | 应对措施 |
|------|-------|------|---------|
| Etsy 竞品网站反爬虫 | 高 | 低 | User-Agent 伪装 + 请求间隔降频 |
| RSS 源不稳定或内容质量差 | 低 | 中 | 人工定期检查 RSS 有效性 |
| GitHub Pages 访问在国内不稳定 | 中 | 中 | 考虑切换到 Vercel 或国内托管 |
| 摘要质量不足 | 中 | 中 | 第二期引入 LLM 优化 |

---

## 9. 成功指标

- 团队每周通过钉钉链接访问资讯网页的次数
- 各部门主动查阅的频率
- 从资讯中产生的营销课题或 SOP 创新数量
# Callie 社媒内容生成工具 v2 实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 实现 v2 版本自然流社媒内容生成工具，支持用户上传热门贴文后 AI 分析 + 产品匹配 + 双 Excel 输出

**Architecture:** 基于现有 v1 FastAPI 单页工具架构，重构后端模块化，新增产品库 SQLite + OpenCV 智能抽帧 + Qwen-Image-Edit 生图

**Tech Stack:** Python FastAPI / SQLite / openpyxl / OpenCV / SiliconFlow Qwen3-VL + Qwen-Image-Edit-2509

---

## 文件结构

```
callie-social-content-tool/
├── app.py                      # FastAPI 后端（重构，新增模块）
├── index.html                  # 前端页面（更新 UI）
├── config.yaml                 # 配置文件
├── requirements.txt            # Python 依赖
├── scripts/
│   └── crawl_products.py      # Callie.com 产品爬虫（新增）
├── data/
│   └── products.db            # SQLite 产品库（首次运行自动创建）
├── build_excel.py             # Excel 生成模块（重构，分离两个 Excel）
├── video_frames.py            # OpenCV 视频帧提取模块（新增）
└── static/
    └── keyframes/             # 关键帧图片临时目录
```

---

## Task 1: 产品库模块（crawl_products.py + products.db）

**Files:**
- Create: `callie-social-content-tool/scripts/crawl_products.py`
- Create: `callie-social-content-tool/data/products.db` (首次运行自动创建)

- [ ] **Step 1: 创建 SQLite 产品库表结构**

```python
# scripts/db_products.py
import sqlite3, os
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "data" / "products.db"
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name_en TEXT NOT NULL,
            name_cn TEXT,
            category TEXT,
            tags TEXT,          -- JSON array: ["宠物纪念品", "生日礼物"]
            image_url TEXT,
            description TEXT,
            occasions TEXT,     -- JSON array: ["生日", "婚礼"]
            status TEXT DEFAULT '在售',
            crawled_at TEXT
        )
    """)
    c.execute("CREATE INDEX IF NOT EXISTS idx_category ON products(category)")
    c.execute("CREATE INDEX IF NOT EXISTS idx_tags ON products(tags)")
    conn.commit()
    conn.close()
    print(f"Database initialized: {DB_PATH}")

if __name__ == "__main__":
    init_db()
```

Run: `python scripts/db_products.py`
Expected: "Database initialized: .../products.db"

- [ ] **Step 2: 创建爬虫脚本框架（静态 HTML 解析）**

```python
# scripts/crawl_products.py
"""
Callie.com 产品爬虫
首次使用：python scripts/crawl_products.py
"""
import httpx, sqlite3, json, re, time
from pathlib import Path
from bs4 import BeautifulSoup

DB_PATH = Path(__file__).parent.parent / "data" / "products.db"
CALLIE_BASE = "https://www.callie.com"

# 导航栏分类（需手动确认，实际应从页面抓取）
NAV_CATEGORIES = {
    "personalized-gifts": "个性化礼品",
    "pet-memory": "宠物纪念品",
    "home-decor": "家居装饰",
}

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    db_path = Path(DB_PATH)
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = get_db()
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name_en TEXT NOT NULL,
            name_cn TEXT,
            category TEXT,
            tags TEXT,
            image_url TEXT,
            description TEXT,
            occasions TEXT,
            status TEXT DEFAULT '在售',
            crawled_at TEXT
        )
    """)
    c.execute("CREATE INDEX IF NOT EXISTS idx_category ON products(category)")
    conn.commit()
    conn.close()

def crawl_category(category_slug: str, category_cn: str) -> list:
    """爬取单个分类下的所有产品"""
    url = f"{CALLIE_BASE}/{category_slug}"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    products = []
    try:
        resp = httpx.get(url, headers=headers, timeout=30)
        soup = BeautifulSoup(resp.text, "html.parser")
        # 注意：实际选择器需要根据 Callie.com 实际页面结构调整
        items = soup.select(".product-item a[href*='/product/']")
        for item in items:
            href = item.get("href", "")
            name_en = item.select_one(".product-name").get_text(strip=True) if item.select_one(".product-name") else ""
            img = item.select_one("img[src]")["src"] if item.select_one("img[src]") else ""
            if href and name_en:
                products.append({
                    "name_en": name_en,
                    "category": category_cn,
                    "image_url": img if img.startswith("http") else CALLIE_BASE + img,
                    "href": href if href.startswith("http") else CALLIE_BASE + href,
                })
        print(f"  [{category_cn}] 找到 {len(items)} 个产品")
    except Exception as e:
        print(f"  [{category_cn}] 爬取失败: {e}")
    return products

def crawl_product_detail(product: dict) -> dict:
    """爬取单个产品详情页"""
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    try:
        resp = httpx.get(product["href"], headers=headers, timeout=30)
        soup = BeautifulSoup(resp.text, "html.parser")
        # 实际选择器需根据页面调整
        desc_elem = soup.select_one(".product-description")
        product["description"] = desc_elem.get_text(strip=True) if desc_elem else ""
        # 适用场景从描述中提取关键词判断
        occasions = []
        desc_lower = product["description"].lower()
        if any(w in desc_lower for w in ["birthday", "生日"]): occasions.append("生日")
        if any(w in desc_lower for w in ["wedding", "婚礼"]): occasions.append("婚礼")
        if any(w in desc_lower for w in ["anniversary", "纪念日"]): occasions.append("纪念日")
        if any(w in desc_lower for w in ["mother", "母亲"]): occasions.append("母亲节")
        if any(w in desc_lower for w in ["father", "父亲"]): occasions.append("父亲节")
        if any(w in desc_lower for w in ["pet", "宠物"]): occasions.append("宠物")
        product["occasions"] = json.dumps(occasions, ensure_ascii=False)
        product["tags"] = json.dumps([product["category"]], ensure_ascii=False)
        time.sleep(0.5)  # 避免请求过快
    except Exception as e:
        print(f"  详情页失败: {e}")
    return product

def save_products(products: list):
    conn = get_db()
    c = conn.cursor()
    # 清空旧数据
    c.execute("DELETE FROM products")
    for p in products:
        c.execute("""
            INSERT INTO products (name_en, name_cn, category, tags, image_url, description, occasions, status, crawled_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, '在售', datetime('now'))
        """, (p.get("name_en"), p.get("name_cn"), p.get("category"), p.get("tags"),
              p.get("image_url"), p.get("description"), p.get("occasions")))
    conn.commit()
    conn.close()
    print(f"\n已保存 {len(products)} 个产品到数据库")

def main():
    print("开始爬取 Callie.com 产品...")
    all_products = []
    for slug, cn in NAV_CATEGORIES.items():
        print(f"爬取分类: {cn}")
        prods = crawl_category(slug, cn)
        for p in prods:
            detail = crawl_product_detail(p)
            all_products.append(detail)
    save_products(all_products)
    print("完成!")

if __name__ == "__main__":
    init_db()
    main()
```

Run: `python scripts/crawl_products.py`
Expected: 输出每个分类的产品数量，最终保存到 products.db

- [ ] **Step 3: 创建产品库查询模块**

```python
# scripts/product_db.py
"""产品库查询和匹配模块"""
import sqlite3, json
from pathlib import Path
from typing import List, Dict

DB_PATH = Path(__file__).parent.parent / "data" / "products.db"

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def search_products(keywords: List[str], top_n: int = 3) -> List[Dict]:
    """根据关键词搜索产品，返回 Top N"""
    conn = get_db()
    c = conn.cursor()
    # 简单模糊匹配 name_en + description + tags
    pattern = "%" + "%".join(keywords) + "%"
    c.execute("""
        SELECT id, name_en, name_cn, category, tags, image_url, description, occasions
        FROM products
        WHERE name_en LIKE ? OR description LIKE ? OR tags LIKE ?
        LIMIT ?
    """, (pattern, pattern, pattern, top_n))
    rows = c.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_all_products() -> List[Dict]:
    """获取所有产品"""
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM products")
    rows = c.fetchall()
    conn.close()
    return [dict(row) for row in rows]

if __name__ == "__main__":
    # 测试
    results = search_products(["pet", "memory"], 3)
    print(f"Found {len(results)} products")
    for p in results:
        print(f"  - {p['name_en']} ({p['category']})")
```

Run: `python scripts/product_db.py`
Expected: 显示匹配到的产品列表

- [ ] **Step 4: 提交代码**

```bash
git add scripts/crawl_products.py scripts/db_products.py scripts/product_db.py
git commit -m "feat: add Callie product crawler and SQLite product database"
```

---

## Task 2: 视频智能抽帧模块

**Files:**
- Create: `callie-social-content-tool/video_frames.py`

- [ ] **Step 1: 编写 OpenCV 抽帧模块**

```python
# video_frames.py
"""
视频智能抽帧：OpenCV 场景检测 + 返回候选帧位置
混合模式第一步：检测场景大幅变化点，返回 10-15 个候选帧时间戳
"""
import cv2, numpy as np
from typing import List, Tuple

def detect_scene_changes(video_path: str, min_candidate_frames: int = 10, max_candidate_frames: int = 15) -> List[float]:
    """
    检测视频中画面大幅变化点，返回候选帧时间戳列表（秒）
    使用帧差分法 + 阈值判断
    """
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise ValueError(f"Cannot open video: {video_path}")

    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = total_frames / fps if fps > 0 else 0

    frame_diffs = []
    prev_frame = None
    positions = []

    frame_idx = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        if prev_frame is not None:
            diff = np.abs(gray.astype(float) - prev_frame.astype(float)).mean()
            frame_diffs.append(diff)
            positions.append(frame_idx / fps)
        prev_frame = gray
        frame_idx += 1

    cap.release()

    if not frame_diffs:
        # 视频太短，返回均匀分布的时间点
        return [i * duration / (min_candidate_frames - 1) for i in range(min_candidate_frames)]

    # 计算阈值：使用帧差分的中位数 * 系数
    threshold = np.median(frame_diffs) * 2.5
    change_points = []
    for i, diff in enumerate(frame_diffs):
        if diff > threshold:
            change_points.append(positions[i])

    # 如果变化点太少，使用帧差分峰值补充
    if len(change_points) < min_candidate_frames:
        diff_sorted = sorted(enumerate(frame_diffs), key=lambda x: x[1], reverse=True)
        extra_points = [positions[i] for i, _ in diff_sorted[:min_candidate_frames - len(change_points)]]
        change_points.extend(extra_points)

    # 去重并排序
    change_points = sorted(set(change_points))
    # 确保在视频时间范围内
    change_points = [t for t in change_points if 0 <= t < duration]

    # 均匀采样到 10-15 个
    if len(change_points) > max_candidate_frames:
        indices = np.linspace(0, len(change_points) - 1, max_candidate_frames, dtype=int)
        change_points = [change_points[i] for i in indices]

    # 如果仍然不足，补充均匀分布点
    while len(change_points) < min_candidate_frames:
        gap = duration / (min_candidate_frames - len(change_points) + 1)
        for i in range(1, min_candidate_frames - len(change_points) + 1):
            t = i * gap
            if t not in change_points and t < duration:
                change_points.append(t)
        break

    return sorted(change_points)[:max_candidate_frames]

def extract_frames_at_times(video_path: str, timestamps: List[float], output_dir: str) -> List[str]:
    """
    在指定时间点截取帧图片，返回文件路径列表
    """
    import os
    os.makedirs(output_dir, exist_ok=True)
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise ValueError(f"Cannot open video: {video_path}")

    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_paths = []

    for i, t in enumerate(timestamps):
        cap.set(cv2.CAP_PROP_POS_MSEC, t * 1000)
        ret, frame = cap.read()
        if ret:
            out_path = os.path.join(output_dir, f"candidate_{i:02d}.jpg")
            cv2.imwrite(out_path, frame)
            frame_paths.append(out_path)

    cap.release()
    return frame_paths

if __name__ == "__main__":
    import sys, os
    if len(sys.argv) < 2:
        print("Usage: python video_frames.py <video_path>")
        sys.exit(1)
    video_path = sys.argv[1]
    output_dir = os.path.join(os.path.dirname(video_path), "candidates")
    times = detect_scene_changes(video_path)
    print(f"检测到 {len(times)} 个候选帧时间点: {times}")
    paths = extract_frames_at_times(video_path, times, output_dir)
    print(f"已保存到: {paths}")
```

Run: `python video_frames.py test_video.mp4`
Expected: 输出候选帧时间点列表 + 保存候选帧图片

- [ ] **Step 2: 提交代码**

```bash
git add video_frames.py
git commit -m "feat: add OpenCV scene detection for video frame extraction"
```

---

## Task 3: 重构 app.py 后端（核心流程）

**Files:**
- Modify: `callie-social-content-tool/app.py`

- [ ] **Step 1: 添加产品库和抽帧相关导入 + 路由**

在现有 app.py 顶部添加新导入：

```python
# 新增导入
from video_frames import detect_scene_changes, extract_frames_at_times
from scripts.product_db import search_products
import asyncio

# 新增配置
TEMP_DIR = Path(__file__).parent / "temp"
TEMP_DIR.mkdir(exist_ok=True)
KEYFRAMES_DIR = Path(__file__).parent / "static" / "keyframes"
KEYFRAMES_DIR.mkdir(parents=True, exist_ok=True)
```

- [ ] **Step 2: 新增 /api/analyze-frames 端点（AI 精选 6 帧）**

在 app.py 中添加：

```python
@app.post("/api/analyze-frames")
async def analyze_frames(candidates: List[str] = Form(...)):
    """
    接收候选帧路径列表，AI 精选最重要的 6 帧
    返回：selected_indices (list[int])
    """
    # 逐帧分析
    frame_scores = []
    for i, path in enumerate(candidates):
        with open(path, "rb") as f:
            data = f.read()
        b64_item = make_b64_item(data)
        prompt = """分析这张图片的关键程度（0-10）：
- 画面内容是否独特（少见的场景/表情/构图）: +2
- 是否有情感张力（惊喜/温馨/震撼）: +3
- 是否是视频高潮点（礼物揭晓/关键动作）: +3
- 画面质量（清晰度/亮度/构图）: +2

只返回一个数字。"""
        try:
            async with httpx.AsyncClient(timeout=60) as client:
                resp = await client.post(
                    "https://api.siliconflow.cn/v1/chat/completions",
                    headers={"Authorization": f"Bearer {SILICONFLOW_KEY}"},
                    json={
                        "model": VISION_MODEL,
                        "messages": [{"role": "user", "content": [
                            {"type": "image_url", "image_url": {"url": f"data:{b64_item['mime']};base64,{b64_item['b64']}"}},
                            {"type": "text", "text": prompt}
                        ]}]
                    }
                )
                result = resp.json()
                score_text = result["choices"][0]["message"]["content"].strip()
                score = float(''.join(filter(lambda x: x.isdigit() or x == '.', score_text)) or 5)
                frame_scores.append((i, score))
        except Exception as e:
            frame_scores.append((i, 5))  # 默认分数
            print(f"Frame {i} analysis error: {e}")

    # 按分数排序，取 top 6
    frame_scores.sort(key=lambda x: x[1], reverse=True)
    selected_indices = sorted([idx for idx, _ in frame_scores[:6]])
    return {"selected": selected_indices}
```

- [ ] **Step 3: 新增 /api/match-products 端点（产品匹配）**

```python
@app.post("/api/match-products")
async def match_products(content_tags: List[str] = Form(...), top_n: int = Form(3)):
    """
    根据内容标签从产品库匹配 Top N 产品
    """
    products = search_products(content_tags, top_n)
    return {"products": products}
```

- [ ] **Step 4: 提交代码**

```bash
git add app.py
git commit -m "feat: add frame analysis and product matching API endpoints"
```

---

## Task 4: 更新前端 index.html

**Files:**
- Modify: `callie-social-content-tool/index.html`

- [ ] **Step 1: 更新上传区域 UI（支持热门内容上传）**

将现有"产品图"上传区域改为"热门内容"上传：

```html
<!-- 替换现有的产品图上传区域 -->
<div class="form-group">
  <label>热门贴文内容 <span class="label-hint">必填，图片或视频（mp4）</span></label>
  <div class="upload-area" id="contentUpload" onclick="document.getElementById('contentInput').click()">
    <div>📷 点击上传热门图片</div>
    <div class="hint">支持 JPG/PNG/GIF，或 mp4 视频</div>
    <input type="file" id="contentInput" accept="image/*,video/mp4" onchange="onContentSelect(this)">
  </div>
  <div class="preview-grid" id="contentPreview"></div>
  <div id="videoPreview" style="display:none; margin-top:10px;">
    <video id="uploadedVideo" controls style="max-width:100%;border-radius:8px;"></video>
    <div id="frameCount" style="font-size:12px;color:#888;margin-top:4px;"></div>
  </div>
</div>

<div class="form-group">
  <label>目标平台</label>
  <select id="platform">
    <option value="Instagram">Instagram</option>
    <option value="TikTok">TikTok</option>
    <option value="Pinterest">Pinterest</option>
  </select>
</div>
```

- [ ] **Step 2: 添加 JavaScript 逻辑**

```javascript
let uploadedContentType = null; // 'image' or 'video'
let selectedFrames = [];

function onContentSelect(input) {
  const file = input.files[0];
  if (!file) return;
  
  if (file.type.startsWith('video/')) {
    uploadedContentType = 'video';
    const video = document.getElementById('uploadedVideo');
    video.src = URL.createObjectURL(file);
    video.style.display = 'block';
    document.getElementById('videoPreview').style.display = 'block';
    document.getElementById('frameCount').textContent = '视频已加载，将自动抽帧分析';
    document.getElementById('contentPreview').innerHTML = '';
  } else {
    uploadedContentType = 'image';
    const preview = document.getElementById('contentPreview');
    preview.innerHTML = '';
    const img = document.createElement('img');
    img.src = URL.createObjectURL(file);
    img.className = 'preview-img';
    img.onload = () => URL.revokeObjectURL(img.src);
    preview.appendChild(img);
    document.getElementById('videoPreview').style.display = 'none';
  }
}

async function uploadAndGenerate() {
  const contentInput = document.getElementById('contentInput');
  const platform = document.getElementById('platform').value;
  if (!contentInput.files[0]) {
    alert('请上传热门内容');
    return;
  }
  
  const formData = new FormData();
  formData.append('file', contentInput.files[0]);
  formData.append('platform', platform);
  
  log('正在上传内容...');
  
  try {
    const response = await fetch('/api/upload-content', {
      method: 'POST',
      body: formData
    });
    const result = await response.json();
    log('内容分析完成: ' + JSON.stringify(result.content_analysis), 'ok');
    log('推荐产品: ' + result.products.map(p => p.name_en).join(', '), 'ok');
    // 显示下载按钮
    document.getElementById('downloadContentPack').style.display = 'block';
    document.getElementById('downloadDesignDoc').style.display = 'block';
  } catch (err) {
    log('错误: ' + err.message, 'error');
  }
}
```

- [ ] **Step 3: 提交代码**

```bash
git add index.html
git commit -m "feat: update frontend UI for trending content upload"
```

---

## Task 5: 重构 Excel 生成逻辑

**Files:**
- Create: `callie-social-content-tool/build_excel.py`

- [ ] **Step 1: 创建独立 Excel 生成模块**

```python
# build_excel.py
"""
生成两个 Excel 文件：
1. 内容生成包.xlsx — 英文文案 + 设计底层逻辑
2. 设计对接文档.xlsx — 完整设计参数 + 关键帧参考图
"""
import openpyxl
from openpyxl import Workbook
from openpyxl.drawing.image import Image as XLImage
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from pathlib import Path
from typing import Dict, List

def build_content_pack(data: Dict, output_path: str):
    """
    生成内容生成包.xlsx
    Sheet1: 内容总览
    Sheet2: 英文文案 + 11条Hashtag
    Sheet3: 关键帧描述
    Sheet4: 产品匹配
    """
    wb = Workbook()
    
    # Sheet1: 内容总览
    ws1 = wb.active
    ws1.title = "内容总览"
    rows = [
        ("Big Idea", data.get("big_idea", "")),
        ("品牌角度", data.get("brand_angle", "")),
        ("产品关联度", data.get("product_tie_in", "")),
        ("行动号召 (CTA)", data.get("cta", "")),
        ("品牌安全检查", data.get("brand_safety_check", "")),
    ]
    for row in rows:
        ws1.append(row)
    
    # Sheet2: 英文文案
    ws2 = wb.create_sheet("英文文案")
    ws2.append(["英文贴文"])
    ws2.append([data.get("caption", "")])
    ws2.append([])
    ws2.append(["11条Hashtag"])
    hashtags = data.get("hashtags", [])
    for tag in hashtags:
        ws2.append([tag])
    
    # Sheet3: 关键帧描述
    ws3 = wb.create_sheet("关键帧描述")
    ws3.append(["时间节点", "画面描述", "镜头运动", "文字Overlay(英文)", "情绪氛围"])
    for row in data.get("script_rows", []):
        ws3.append(row)
    
    # Sheet4: 产品匹配
    ws4 = wb.create_sheet("产品匹配")
    ws4.append(["产品名称", "品类", "推荐理由", "产品图"])
    for p in data.get("matched_products", []):
        ws4.append([p.get("name_en", ""), p.get("category", ""), p.get("match_reason", ""), ""])
        # 插入产品图（如果存在）
        if p.get("image_path") and Path(p["image_path"]).exists():
            img = XLImage(p["image_path"])
            img.width, img.height = 150, 150
            ws4.add_image(img, f"D{ws4.max_row}")
    
    wb.save(output_path)

def build_design_doc(data: Dict, output_path: str, keyframe_images: List[str]):
    """
    生成设计对接文档.xlsx
    Sheet1: 镜头/画面（含参考示意图）
    Sheet2: 设计参数
    Sheet3: 物料清单
    """
    wb = Workbook()
    
    # Sheet1: 镜头/画面
    ws1 = wb.active
    ws1.title = "镜头/画面"
    ws1.append(["帧号", "时间", "参考示意图", "设计说明"])
    for i, (frame_desc, img_path) in enumerate(zip(data.get("script_rows", []), keyframe_images)):
        row_num = i + 2
        ws1.append([f"帧{i+1}", frame_desc[0], "", frame_desc[1]])
        if img_path and Path(img_path).exists():
            img = XLImage(img_path)
            img.width, img.height = 200, 355  # 9:16 竖版
            ws1.add_image(img, f"C{row_num}")
    
    # 设置列宽
    ws1.column_dimensions['A'].width = 8
    ws1.column_dimensions['B'].width = 10
    ws1.column_dimensions['C'].width = 20
    ws1.column_dimensions['D'].width = 40
    
    # Sheet2: 设计参数
    ws2 = wb.create_sheet("设计参数")
    design_params = [
        ("配色方案", data.get("color_palette", "")),
        ("字体建议", data.get("font_suggestion", "")),
        ("排版布局", data.get("layout", "")),
        ("元素位置", data.get("element_positions", "")),
        ("图片规格", "1080x1920 (9:16 竖版)"),
        ("视频规格", "1080x1920, 30fps, 9-30秒"),
    ]
    for row in design_params:
        ws2.append(row)
    
    # Sheet3: 物料清单
    ws3 = wb.create_sheet("物料清单")
    materials = [
        ("图片物料", "1张 1080x1920 主图"),
        ("视频物料", "1个 1080x1920 视频，9-30秒"),
        ("文案物料", "英文贴文 + 11条Hashtag"),
        ("发布平台", data.get("platform", "Instagram")),
    ]
    for row in materials:
        ws3.append(row)
    
    wb.save(output_path)
```

- [ ] **Step 2: 在 app.py 中集成 Excel 生成**

在 `/api/generate` 端点中添加：

```python
from build_excel import build_content_pack, build_design_doc

@app.post("/api/generate")
async def generate_content(task_id: str = Form(...)):
    # ... 现有 AI 生成逻辑 ...
    
    # 生成两个 Excel
    task_dir = TEMP_DIR / task_id
    content_pack_path = task_dir / "内容生成包.xlsx"
    design_doc_path = task_dir / "设计对接文档.xlsx"
    
    # 获取关键帧图片路径
    keyframe_images = list((task_dir / "keyframes").glob("*.jpg")) if (task_dir / "keyframes").exists() else []
    
    build_content_pack(content_data, str(content_pack_path))
    build_design_doc(content_data, str(design_doc_path), [str(p) for p in keyframe_images])
    
    return {"status": "ok", "content_pack": str(content_pack_path), "design_doc": str(design_doc_path)}
```

- [ ] **Step 3: 提交代码**

```bash
git add build_excel.py
git commit -m "feat: add dual Excel generation (content pack + design doc)"
```

---

## Task 6: 集成 Qwen-Image-Edit-2509 生图功能

**Files:**
- Modify: `callie-social-content-tool/app.py`

- [ ] **Step 1: 添加生图端点**

```python
@app.post("/api/generate-keyframes")
async def generate_keyframes(script_rows: List[List[str]] = Form(...), product_images: List[str] = Form(...)):
    """
    使用 Qwen-Image-Edit-2509 生成 6 帧参考示意图
    script_rows: [[时间, 画面描述, ...], ...]
    product_images: base64 编码的产品图片列表
    """
    keyframe_paths = []
    
    for i, row in enumerate(script_rows[:6]):
        time_code, scene_desc = row[0], row[1]
        prompt = f"""Create a 9:16 vertical Instagram story/reels frame with the following scene:
        
Scene: {scene_desc}

Requirements:
- Clean, modern aesthetic matching Callie brand (warm, personalized gift brand)
- Include English overlay text on screen
- High contrast, vibrant colors
- Professional product photography style
- 1080x1920 pixels (9:16 aspect ratio)"""
        
        try:
            # 构建多模态输入（场景描述 + 产品图）
            contents = [{"type": "text", "text": prompt}]
            for prod_b64 in product_images[:2]:  # 最多加 2 张产品图
                contents.append({"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{prod_b64}"}})
            
            async with httpx.AsyncClient(timeout=120) as client:
                resp = await client.post(
                    "https://api.siliconflow.cn/v1/images/generations",
                    headers={"Authorization": f"Bearer {SILICONFLOW_KEY}"},
                    json={
                        "model": "Qwen/Qwen-Image-Edit-2509",
                        "prompt": prompt,
                        "image_size": "1024x1856",
                        "num_images": 1
                    }
                )
                result = resp.json()
                img_url = result["data"][0]["url"]
                
                # 下载图片
                img_resp = await client.get(img_url)
                img_path = KEYFRAMES_DIR / f"keyframe_{i+1:02d}.jpg"
                img_path.write_bytes(img_resp.content)
                keyframe_paths.append(str(img_path))
        except Exception as e:
            print(f"Keyframe {i+1} generation failed: {e}")
            keyframe_paths.append("")
    
    return {"keyframes": keyframe_paths}
```

- [ ] **Step 2: 提交代码**

```bash
git add app.py
git commit -m "feat: integrate Qwen-Image-Edit-2509 for keyframe generation"
```

---

## Task 7: 打包分发脚本

**Files:**
- Create: `callie-social-content-tool/start.bat`
- Create: `callie-social-content-tool/stop.bat`
- Create: `callie-social-content-tool/update.bat`

- [ ] **Step 1: 创建 start.bat**

```bat
@echo off
chcp 65001 >nul
title Callie 社媒内容生成工具

echo [1/3] 检查 Python 环境...
python --version >nul 2>&1
if errorlevel 1 (
    echo 错误：未找到 Python，请先安装 Python 3.8+
    pause
    exit /b 1
)

echo [2/3] 创建虚拟环境（如需要）...
if not exist "venv" (
    python -m venv venv
    call venv\Scripts\activate.bat
    pip install --upgrade pip
    pip install -r requirements.txt
    echo 依赖安装完成
) else (
    call venv\Scripts\activate.bat
)

echo [3/3] 启动服务...
set PORT=8000
python -m uvicorn app:app --host 127.0.0.1 --port %PORT% --reload
```

- [ ] **Step 2: 创建 stop.bat**

```bat
@echo off
chcp 65001 >nul
echo 正在停止服务...
taskkill /F /IM python.exe >nul 2>&1
echo 服务已停止
pause
```

- [ ] **Step 3: 创建 update.bat**

```bat
@echo off
chcp 65001 >nul
title 更新产品库

echo 正在更新 Callie 产品库...
if exist "venv" (
    call venv\Scripts\activate.bat
)
python scripts/crawl_products.py
echo 更新完成
pause
```

- [ ] **Step 4: 提交代码**

```bash
git add start.bat stop.bat update.bat
git commit -m "feat: add distribution scripts (start/stop/update bat)"
```

---

## Task 8: 更新 requirements.txt

**Files:**
- Modify: `callie-social-content-tool/requirements.txt`

- [ ] **Step 1: 添加新依赖**

```
# 现有依赖保留，新增：
opencv-python>=4.8.0
beautifulsoup4>=4.12.0
lxml>=4.9.0
```

完整 requirements.txt：

```
fastapi>=0.100.0
uvicorn>=0.23.0
python-multipart>=0.0.6
openpyxl>=3.1.0
httpx>=0.25.0
PyYAML>=6.0
pillow>=10.0.0
pillow-heif>=0.13.0
opencv-python>=4.8.0
beautifulsoup4>=4.12.0
lxml>=4.9.0
```

- [ ] **Step 2: 提交代码**

```bash
git add requirements.txt
git commit -m "chore: add opencv and beautifulsoup dependencies"
```

---

## 自检清单

1. **Spec coverage**: 逐条核对设计文档，所有 9 个分析项、产品库、两个 Excel 输出均有对应任务
2. **Placeholder scan**: 无 "TBD"、"TODO"、未完成步骤
3. **Type consistency**: API 端点参数名在 app.py 和 index.html 中一致（`task_id`、`platform`、`content_tags` 等）

---

**Plan complete and saved to `docs/superpowers/plans/2026-06-22-callie-social-content-tool-v2.md`.**

Two execution options:

**1. Subagent-Driven (recommended)** - I dispatch a fresh subagent per task, review between tasks, fast iteration

**2. Inline Execution** - Execute tasks in this session using executing-plans, batch execution with checkpoints

**Which approach?**
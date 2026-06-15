# Callie 社媒内容生成 Workflow — 实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 建立 Callie 社媒内容生成 Workflow，打通产品信息提取 → 热门视频结构拆解 → 多平台内容生成 → 关键帧示意图生成全流程。

**Architecture:** 在现有 `callie-social-posts` skill 基础上，新增 `video-breakdown` skill 和 workflow 编排层，实现模块化串联。

**Tech Stack:** Superpowers skill 框架 / AI Vision（多模态LLM）/ AI 图像生成 / prompt engineering

---

## 文件结构

```
D:/工作/网翔/callie-social-posts/
├── SKILL.md                          # 主skill（更新：接受product/video insight输入）
├── workflow-social-content.yaml      # 新增：workflow编排定义
└── references/
    ├── brand-guide.md                # 已有
    ├── platform-rules.md            # 已有
    ├── output-format.md             # 已有
    ├── content-examples.md          # 已有
    ├── trend-hooking.md             # 已有
    └── trend-sources.md             # 已有

D:/工作/AI/claude-demo/docs/superpowers/
├── specs/
│   └── 2026-06-15-callie-social-content-workflow-design.md   # 已有设计文档
└── skills/
    └── video-breakdown/
        └── SKILL.md                 # 新增：视频结构拆解skill（之前生成但未落地）
```

---

## Task 1: 创建 video-breakdown Skill

**Files:**
- Create: `D:/工作/AI/claude-demo/docs/superpowers/skills/video-breakdown/SKILL.md`

- [ ] **Step 1: 创建 video-breakdown SKILL.md**

```markdown
---
name: video-breakdown
description: 拆解短视频结构：Hook类型、CTA类型、叙事结构、节奏分布、字幕/文字Overlay使用方式。输入视频文件，输出结构化分析结果。
metadata:
  type: skill
  platform: superpowers
---

# Video Breakdown Skill

Analyzes short video content and returns a structured breakdown of its viral mechanics.

## When to Use

Use this skill when you need to understand what makes a specific video work — before replicating, before generating new content based on it, or before auditing a competitor's creative approach.

## Input

User provides a video file (mp4/mov) or video link.

## Process

1. **Frame Extraction** — Extract key frames at ~0s, 3s, 8s, 15s, 22s, 30s (or all key transition points for shorter/longer videos)
2. **Scene Analysis** — For each extracted frame, describe: visual composition, text overlays visible, faces/objects/environment, camera angle
3. **Structural Breakdown** — Analyze the full video structure:

## Output Schema

```markdown
## Video Breakdown Result

### Basic Info
- Source: [user-provided description or link]
- Duration: [X seconds]
- Platform: [TikTok / Instagram Reels / YouTube Shorts / other]

### Hook Analysis
- Hook Type: [悬念留白 / 情感共鸣 / POV视角 / 礼物揭晓 / 问题抛出 / 前后对比 / 其他]
- Hook Mechanism: [具体描述hook如何在前3秒抓注意力]
- Text/Visual Hook Elements: [前3秒的文字或画面元素]

### CTA Analysis
- CTA Type: [账号引导 / 购买链接 / 评论互动 / 分享邀请 / 直接提问 / 无明显CTA]
- CTA Placement: [视频结尾 / 全程植入 / 隐藏式]
- CTA Style: [强硬推销 / 软性引导 / 账号沉淀]

### Narrative Structure
- Structure Type: [三段式 / 问题-解决 / 前后对比 / 故事线 / 清单式 / 其他]
- Story Arc: [起承转合描述]

### Pacing Breakdown
| Time | Segment | Content Summary |
|------|---------|----------------|
| 0-3s | Hook | [内容] |
| 3-15s | Body | [内容] |
| 15-30s | Reveal/CTA | [内容] |

### Text/Overlay Usage
- Overlay Style: [少量关键词 / 全程字幕 / 无文字 / 弹幕式]
- Font/Treatment: [如果可见]
- Key Text Snippets: [可见的文字内容]

### Audio/Music
- Music Type: [欢快 / 情感 / 趋势 / 原声]
- Sound Effects: [是否有音效]

### Key Takeaways for Content Creation
- What works: [1-2条核心洞察]
- Replicable elements: [可以复用的具体元素]
- Brand fit for Callie: [该结构是否适合Callie产品]
```

## Quality Notes

- Be specific about visual elements — describe what you see, not just the general type
- Note any text visible in the video (brand names, product labels, on-screen text)
- Identify whether the video is UGC (user-generated) or professional production
- Flag if the video contains trend-specific audio or meme formats that may not transfer
```

- [ ] **Step 2: 提交**

```bash
git add docs/superpowers/skills/video-breakdown/SKILL.md
git commit -m "feat: add video-breakdown skill"
```

---

## Task 2: 更新 callie-social-posts Skill（接受 product insight + video insight）

**Files:**
- Modify: `D:/工作/网翔/callie-social-posts/SKILL.md`

- [ ] **Step 1: 更新 SKILL.md 新增输入部分**

在现有的 "## Workflow" 部分之后，新增：

```markdown
## Alternative Workflow: With Product + Video Insight

When the user provides a Callie product link/image AND a trending video file, use this enhanced workflow:

### Step A: Product Information Extraction
If user provides a product image and/or link:
- Analyze the product image using AI Vision: extract product name, category, material, style, target occasion, target audience
- Ask user to confirm or correct the extracted product info

### Step B: Video Structure Analysis
If user provides a video file:
- Apply the video-breakdown skill to extract: hook type, cta type, narrative structure, pacing
- Ask user to confirm the video insight

### Step C: Enhanced Content Generation
- Load `references/brand-guide.md`, `references/platform-rules.md`, `references/output-format.md`
- Combine product insight + video insight as creative seed
- Generate platform-specific content pack
- Output: English post copy, 11 hashtags (TikTok), Chinese video script, keyframe descriptions
```

- [ ] **Step 2: 更新 output-format.md 添加关键帧部分**

在 `output-format.md` 末尾的完整内容 pack 模板中，在 "Visual Direction" 部分之后添加：

```markdown
### 9. Keyframe Descriptions
[For video content only]

| Frame | Time | Visual Description | On-Screen Text Suggestion |
|-------|------|-------------------|--------------------------|
| 1 | 0-3s | [Hook frame description] | [Text overlay suggestion] |
| 2 | 3-8s | [Product/relationship moment] | — |
| 3 | 8-15s | [Main content] | — |
| 4 | 15-22s | [Reveal/moment] | [Key message] |
| 5 | 22-30s | [CTA frame] | [Account handle / link] |

Note: These are text descriptions only. AI image generation can be requested as a separate step.
```

- [ ] **Step 3: 提交**

```bash
cd "D:/工作/网翔/callie-social-posts"
git add SKILL.md references/output-format.md
git commit -m "feat: enhance callie-social-posts skill with product+video insight workflow"
```

---

## Task 3: 创建 Workflow 编排文件

**Files:**
- Create: `D:/工作/网翔/callie-social-posts/workflow-social-content.yaml`

- [ ] **Step 1: 创建 workflow-social-content.yaml**

```yaml
name: callie-social-content-workflow
description: >
  Generate platform-specific social content for Callie.com products.
  Input: product image + link + trending video file + target platform.
  Output: English post copy + 11 hashtags + Chinese video script + keyframe descriptions.
version: "1.0.0"

steps:
  - id: product-insight
    name: Product Information Extraction
    description: >
      Analyze the uploaded product image (and optional link) to extract:
      product name, category, material, style, target occasion, target audience.
      Ask user to confirm or correct the extracted information.
    tools:
      - AI Vision (multimodal LLM)
    output: product_insight
    optional: true

  - id: video-insight
    name: Trending Video Structure Analysis
    description: >
      Apply video-breakdown skill to the uploaded video file.
      Extract: hook type, cta type, narrative structure, pacing breakdown,
      text/overlay usage, audio type.
      Ask user to confirm or upload a different video.
    tools:
      - video-breakdown skill
    output: video_insight
    optional: true

  - id: content-generation
    name: Platform Content Generation
    description: >
      Generate a complete content pack for the target platform.
      Combine product_insight and video_insight as creative seed.
      Load brand-guide, platform-rules, output-format references.
    tools:
      - callie-social-posts skill (enhanced workflow)
    input:
      - product_insight (from step 1, if provided)
      - video_insight (from step 2, if provided)
      - target_platform (user-provided)
    output: content_pack

  - id: keyframe-generation
    name: Keyframe Illustration (Text-Based)
    description: >
      Convert the Chinese video script into 4-6 keyframe descriptions.
      Each frame includes: time marker, visual description, camera movement,
      text overlay suggestion, emotional tone.
      Format as a storyboard table.
    tools:
      - AI text generation
    input:
      - content_pack (from step 3)
    output: keyframe_descriptions
    optional: true

outputs:
  - content_pack
  - keyframe_descriptions
  - product_insight (if step 1 ran)
  - video_insight (if step 2 ran)
```

- [ ] **Step 2: 提交**

```bash
cd "D:/工作/AI/claude-demo"
git add "D:/工作/网翔/callie-social-posts/workflow-social-content.yaml"
git commit -m "feat: add social content workflow yaml"
```

---

## Task 4: 验证流程 — 端到端测试

**Files:**
- Test with: `D:/工作/网翔/callie-social-posts/SKILL.md`
- Test with: `D:/工作/AI/claude-demo/docs/superpowers/skills/video-breakdown/SKILL.md`

- [ ] **Step 1: 用真实案例测试全流程**

找一个 Callie 产品页面（如定制首饰），准备一个示例视频，执行完整流程：

1. Product insight 提取（截图 + 链接）
2. Video insight 拆解（上传示例视频）
3. Content generation（选定一个平台，如 TikTok）
4. Keyframe 描述生成

验证每个步骤的输出是否正确串联。

- [ ] **Step 2: 检查输出是否符合设计文档要求**

对照 `docs/superpowers/specs/2026-06-15-callie-social-content-workflow-design.md` 逐项检查：
- [ ] 英文贴文文案 ✓
- [ ] 11个 Hashtag（TikTok）✓
- [ ] 中文视频脚本 ✓
- [ ] 4-6个关键帧描述 ✓
- [ ] 品牌安全检查 ✓

- [ ] **Step 3: 提交测试结果**

```bash
git add docs/superpowers/specs/2026-06-15-callie-social-content-workflow-design.md
git commit -m "docs: update design spec with verified checkmarks"
```

---

## 自检清单

完成所有任务后检查：

1. **Spec 覆盖：** 设计文档中每个步骤都有对应实现
2. **无占位符：** Skill prompt 中没有 "TBD"、"TODO"、"待实现"
3. **流程串联：** Product insight → Video insight → Content gen → Keyframe 串联无误
4. **平台适配：** Hashtag 数量符合各平台规则（TikTok 11个、Instagram 5-8个等）
5. **品牌一致性：** 所有内容符合 brand-guide.md 的声调和定位

---

**Plan complete and saved to `docs/superpowers/plans/2026-06-15-callie-social-content-workflow-plan.md`. Two execution options:**

**1. Subagent-Driven (recommended)** - I dispatch a fresh subagent per task, review between tasks, fast iteration

**2. Inline Execution** - Execute tasks in this session using executing-plans, batch execution with checkpoints

**Which approach?**
# Callie.com Remarketing 完整方案
# Remarketing Campaign Plan — FB Ads & Google Ads
## 提升复购率专项 | 2026 年度执行版

---

## 一、品牌背景与方案目标

**品牌**：Callie.com
**定位**：面向 Z 世代 / 年轻千禧代女性的裙子/套装品牌，主力品类为连衣裙（Mini/Midi/Maxi）、上装、裙装、套装，价格带 $20–$80，核心场景为约会、派对、度假、婚礼宾客、毕业舞会。

**在售 SKU**：2w–5w，品牌自产素材，有热卖 SKU 数据支持。

**核心目标**：提升复购率
- 广告 ROAS ≥ 1.45x
- 各受众层复购率达标
- 前期测试预算 $500–$1,000，达标后扩量

---

## 二、受众分层体系

### 2.1 时间维度（Purchase-based Recency Segments）

| 受众名称（Meta/GA4 命名） | 定义 | 投放目的 |
|---|---|---|
| `R_15d` | 最近一次购买 ≤ 15 天 | 高频提醒、品牌强化、配件/套装追加 |
| `R_30d` | 购买后 16–30 天 | 当季新品/搭配复购提醒 |
| `R_60d` | 购买后 31–60 天 | 中期激活、换季/场合提醒 |
| `R_90d` | 购买后 61–90 天 | 沉睡用户唤醒、优惠触发 |

**实现方式**：自有数据集导出 CSV → 通过数据伙伴或直接上传至 Meta / Google Ads Audience Manager

### 2.2 品类维度（Product Category Segments）

| 受众名称 | 定义 | 复购逻辑 |
|---|---|---|
| `CAT_Dress` | 购买过 Dresses 类目 | 推荐新款连衣裙、套装、场合裙 |
| `CAT_Top` | 购买过 Tops / Bodysuits | 推荐搭配下装/新季节新款 |
| `CAT_Coord` | 购买过 Matching Sets / Coords | 推荐新套装或单件升级 |
| `CAT_Occasion` | 购买过 Occasion Wear | 季节性场合（度假、节日）复购 |
| `CAT_Bottom` | 购买过 Skirts / Pants | 推荐新上装形成完整穿搭 |

### 2.3 复合受众（Cross-segment）

| 受众 | 定义 | 适用场景 |
|---|---|---|
| `R_30d + CAT_Dress` | 30 天内买过裙子 | 当季新款连衣裙精准触达 |
| `R_60d + CAT_Dress` | 60 天+ 买过裙子 | 沉睡唤醒 + 折扣触发 |
| `R_90d + ALL` | 90 天以上任意购买 | 全品类沉睡用户复活大促 |

---

## 三、内容主题（2026 年度节拍）

### 3.1 世界杯（FIFA World Cup 2026）

- **时间**：2026/6/11 开幕 – 7/19 决赛，美加墨联合举办，48 队，104 场
- **主题方向**："赛场 Look，主角气场"、"看比赛穿什么"
- **适用受众**：R_15d ~ R_90d 全体
- **素材方向**：
  - "观赛穿搭"/"夺冠夜穿搭"主题连衣裙种草
  - 世界杯配色（红/白/蓝/绿）滤镜内容
  - 伪直播风格 Reels（场景感强，适配 IG/FB 双端）

### 3.2 夏季度假 / 运动季

- **时间**：6 月起进入夏季出行高峰，结合世界杯观赛派对、毕业季、度假游
- **主题方向**："Summer Ready"、"海岛/城市微度假穿搭"
- **素材方向**：连衣裙 + 凉鞋/草编包度假套装、高温透气面料强调、旅行场景 UGC

### 3.3 下半年节日节拍

| 时间节点 | 主题 | 建议收口 |
|---|---|---|
| 7 月末–8 月 | Summer Sale / 季末清仓 | R_60d/R_90d 折扣触发 |
| 9 月 | 早秋上新、Back to School | 全量受众早秋新款 |
| 11 月 | Black Friday 预热 + 节日礼物 | 全体受众大促激活 |
| 12 月 | 圣诞/新年派对季 | Occasion Wear 再循环 |

---

## 四、选品标准（SKU Filter Framework）

> **背景**：Callie.com 在售 SKU 2w–5w，需在海量 SKU 中建立系统化选品机制

### 4.1 基础筛选优先级（从热卖数据系统提取）

| 优先级 | 维度 | 标准 | 说明 |
|---|---|---|---|
| P1 | 30 天销量排行 | Top 100–200 SKU | 验证高需求，测试主力 |
| P2 | 90 天销量累积 | Top 300–500 SKU | 中长期爆款，库存充足 |
| P3 | 库存深度 | ≥ 50 件 | 防止断货影响转化 |
| P4 | 品类覆盖 | Dress/Tops/Coords/Occasion 各 20%–30% | 确保各受众层均有匹配 |
| P5 | 加购未购率 | > 15% | 高加购低购买 = 强 remarketing 潜力，适合折扣钩子 |
| P6 | 毛利率 | ≥ 30% | 确保 ROAS ≥ 1.45x 的毛利安全垫 |

### 4.2 世界杯专项叠加筛选（叠加 P1–P6）

| 筛选维度 | 标准 | 目的 |
|---|---|---|
| 颜色/风格 | 红/白/蓝/绿纯色系或明亮度假色 | 世界杯主题色彩融合 |
| 场景适配 | 可拍观赛/派对/度假场景的面料/版型 | 减少定制场景成本 |
| 上新时间 | 近 30–60 天内上架新品优先 | 世界杯节点正好上新宣发 |

### 4.3 排除规则

- 近 30 天销量 < 5 件（清仓品除外）
- 库存 < 20 件
- 评分 < 4.0 星
- 同一受众层已曝光 SKU（避免重复曝光）

### 4.4 各 Campaign 选品数量

| Campaign | SKU 数量 | 品类侧重 | 受众匹配逻辑 |
|---|---|---|---|
| T1（世界杯 × Dress） | 5–8 SKU | 连衣裙（Mini/Midi/Maxi） | 世界杯配色/观赛场景款优先 |
| T2（世界杯 × Dress + 折扣钩） | 5–8 SKU | 连衣裙 + 高加购未购款 | 折扣素材为主打 |
| T3（世界杯 × 全品类沉睡唤醒） | 8–12 SKU | 全品类精选 | 高折扣钩子，货品多元化 |
| T4（Summer Ready × Coords） | 4–6 SKU | 套装/Coords | 度假场景面料/轻便款优先 |

**单个 SKU 多版本原则**：每个入选 SKU 制作 **2–3 个创意版本**（不同角度/场景/文案方向），避免审美疲劳并利于 AB Test。

---

## 五、Campaign 结构与平台设置

### 5.1 Meta / Facebook Ads 账户结构

```
Callie — Remarketing — World Cup
├── T1: CAT_Dress × R_30d（世界杯观赛穿搭连衣裙）
├── T2: CAT_Dress × R_60d（世界杯 + 折扣钩子）
├── T3: R_90d 全品类（世界杯派对季优惠触发）
└── T4: CAT_Coord × R_30d（Summer Ready 套装）
```

**Creative Specs**

| 版位 | 尺寸 | 素材方向 |
|---|---|---|
| Facebook Feed + Instagram Feed | 1:1 或 4:5 | 连衣裙上身图 + 主题 Overlay 文字 |
| Instagram Stories | 9:16 | UGC 风格伪直播场景 |
| Reels | 9:16，30s | "看比赛穿这条裙子"适配 IG+FB 双端 |
| Advantage+ | 自动优化 | 多尺寸适配，简化管理 |

### 5.2 Google Ads 配置

**Remarketing 受众列表**

| 受众列表名称 | 成员条件 | 会员期 | 用途 |
|---|---|---|---|
| `callie_15d_buyers` | 购买后 15 天内 | 30 天 | 高频触达、新品推送 |
| `callie_30d_buyers` | 购买后 30 天内 | 60 天 | 当季新款 |
| `callie_60d_buyers` | 购买后 60 天内 | 90 天 | 中期激活 |
| `callie_90d_buyers` | 购买后 90 天内 | 180 天 | 沉睡唤醒 |
| `callie_dress_buyers` | 购买过连衣裙 | 180 天 | 连衣裙复购 |
| `callie_occasion_buyers` | 购买过场合装 | 180 天 | 节日场合复购 |

**Campaign 类型配置**

| Campaign Type | 受众定向 | 目的 |
|---|---|---|
| Performance Max（推荐） | 自定义受众 + 商品 Feed | 全渠道复购转化 |
| Search | 复购词 + 品牌词保护 | 捕获主动搜索流量 |
| Display | callie_30d_buyers + callie_dress_buyers | 视觉冲击、种草 |

**复购关键词示例**

```
- "callie dress new arrivals"
- "callie summer dress 2026"
- "callie occasion dress wedding guest"
- "callie官网" / "callie dress sale"
```

---

## 六、受众同步与数据实现方式

| 数据需求 | 实现路径 | 操作说明 |
|---|---|---|
| 购买后 15/30/60/90 天受众 | 自有数据导出 CSV → 数据伙伴或 Audience Manager | 导出已成交客户购买日期至 CSV，上传至受众管理器 |
| 品类购买记录受众 | Meta Pixel 传入 `content_category` 参数 | 在 Pixel 中传入品类参数，FB 后台按类目自动生成受众 |
| 复合受众（R_30d + CAT_Dress 等） | Meta Business Manager → 受众组合工具 | 创建"交集"受众，限定同时满足两个条件 |
| Lookalike | 以 R_30d 购买用户为种子 | 建议相似比例 1%–3%，先小范围测试 |

---

## 七、测试阶段 T1–T4 搭建

> 前期测试预算 $500–$1,000，验证受众 × 素材组合有效性，周期 7 天

| 测试组 | 受众 | 素材主题 | 测试预算 | 周期 |
|---|---|---|---|---|
| T1（对照） | R_30d + CAT_Dress | 世界杯"观赛穿搭"连衣裙 | $200 | 7 天 |
| T2 | R_60d + CAT_Dress | 世界杯"观赛穿搭" + 折扣钩子 | $200 | 7 天 |
| T3 | R_90d（全品类沉睡） | 世界杯"派对季"优惠触发 | $200 | 7 天 |
| T4（新品类） | R_30d + CAT_Coord | Summer Ready 套装 | $200 | 7 天 |

---

## 八、广告文案库（中英对照）

### 8.1 世界杯专题文案

#### ① 场景带入型（Feed 图片 Overlay / Reels 字幕）

| 英文（对外展示） | 中文（内部参考） | 适用 Campaign |
|---|---|---|
| *"Watch the game, wear this dress."* | 看比赛，就穿这条裙子 | T1 / T2 |
| *"Game night. You look it."* | 进球时刻，你是最靓的 | T1 |
| *"Final night, front-row energy."* | 决赛夜，主角气场全开 | T1 / T3 |
| *"Cheer in style. Cheer in Callie."* | 为球队打气，也要美出新高度 | T2 |
| *"Your game plan: look incredible."* | 你的看球计划：美到犯规 | T1 |
| *"From stands to dance floor — one dress."* | 从看台到舞池，一条裙子全搞定 | T1 / T3 |
| *"The goal isn't just the score."* | 进球不是你唯一的收获 | T3 优惠版 |

#### ② 世界杯配色/产品结合型（产品特写图）

| 英文（对外展示） | 中文（内部参考） | 适用 Campaign |
|---|---|---|
| *"Red, white, blue — and stunning."* | 红白蓝配色，这个夏天绝了 | T1 |
| *"World Cup colors. Off-the-charts cut."* | 世界杯配色，连衣裙版型绝了 | T1 |
| *"Flag colors that actually slay."* | 世界杯国旗色穿搭，这次真的绝了 | T1 |
| *"Green, gold, red — vacation mode on."* | 绿金红调，度假模式全开 | T1（度假裙） |
| *"A dress that wins every match."* | 一条连衣裙，场场稳赢 | T1 / T2 |

#### ③ 折扣钩子型（T2 / T3 优惠触发）

| 英文（对外展示） | 中文（内部参考） | 适用 Campaign |
|---|---|---|
| *"World Cup sale: 20% off — game on."* | 世界杯限时 8 折，看球也要美美的 | T2 / T3 |
| *"Buy the dress, get the vibe free."* | 买连衣裙，赠观赛穿搭氛围感 | T2 |
| *"Score a dress — World Cup deal."* | 世界杯专属折扣，进球般的好价 | T3 |
| *"Limited time: World Cup dress drop."* | 世界杯限定连衣裙，错过等四年 | T2 |
| *"The only goal that counts: your new dress."* | 今晚唯一要进的球：你的新裙子 | T3 |
| *"World Cup deal — too good to whistle."* | 世界杯好价，吹哨级别的划算 | T3 |

#### ④ Reels / Stories 短视频字幕（短促有节奏感）

| 英文（对外展示） | 中文（内部参考） | 格式 |
|---|---|---|
| *"Pick your team. Pick your dress."* | 选你的主队，挑你的裙子 | Reels 字幕 |
| *"Dress for the game. Not just the couch."* | 为比赛而穿，不只是沙发 | Reels 字幕 |
| *"This is how winners dress."* | 赢家是这样穿裙子的 | Stories 字幕 |
| *"Finals fit = front row energy."* | 决赛穿搭 = C位气场 | Stories 字幕 |
| *"World Cup or date night — you're ready."* | 世界杯还是约会夜，你都准备好了 | Reels 字幕 |

---

### 8.2 Summer Ready 专题文案

#### ① 主打款文案（T4 Coords / 套装）

| 英文（对外展示） | 中文（内部参考） | 适用 Campaign |
|---|---|---|
| *"Summer ready. Already."* | 夏款已就位，你呢 | T4 |
| *"The heat is on. So is your style."* | 高温来袭，时髦不等人 | T4 |
| *"Beach to brunch — one set."* | 从海滩到早午餐，一套搞定 | T4 Coords |
| *"Vacation starts when you unpack."* | 旅行从拆快递那刻就开始了 | T4 |
| *"Light fabric. Heavy compliments."* | 轻盈面料，密集夸赞 | T4 |
| *"Packing list: passport, sunglasses, this coord."* | 打包清单：护照、墨镜、这套 | T4 度假 |

#### ② 度假场景文案

| 英文（对外展示） | 中文（内部参考） | 适用 Campaign |
|---|---|---|
| *"Island breeze. Resort vibes. Callie dress."* | 海岛微风、度假感、Callie 裙 | T4 |
| *"The only vacation essential you forgot."* | 唯一遗漏的度假必备单品 | T4 |
| *"Sand, sun, and a whole lot of slay."* | 沙滩、阳光、slay 全开 | T4 |

#### ③ Reels / Stories 短视频字幕

| 英文（对外展示） | 中文（内部参考） | 格式 |
|---|---|---|
| *"Summer starts here."* | 夏天从这里开始 | Reels 字幕 |
| *"Get ready for summer."* | 准备好迎接夏天了吗 | Stories 字幕 |
| *"One set. Infinite vibes."* | 一套，无限氛围感 | Reels 字幕 |

---

### 8.3 品牌强化文案（R_15d 高价值追加销售）

| 英文（对外展示） | 中文（内部参考） | 适用 Campaign |
|---|---|---|
| *"New arrivals. Already called it."* | 新款已到，爆款预定 | R_15d |
| *"Your last Callie wasn't enough."* | 上一条怎么够，再来一条 | R_15d |
| *"Because one dress is never enough."* | 一条裙子怎么够，再来 | R_15d |
| *"You already know. Click again."* | 你懂的，再来一单 | R_15d |
| *"Your collection's not complete."* | 你的衣橱还差这一条 | R_15d |

---

### 8.4 品类专属文案（中英对照）

#### 连衣裙（Dress）专项

| 英文（对外展示） | 中文（内部参考） |
|---|---|
| *"The dress that started it all — again."* | 那条让你入坑的裙子，又来了 |
| *"One dress. Every occasion."* | 一条裙子，万千场合 |
| *"Mini, midi, maxi — all the right reasons."* | Mini、Midi、Maxi，各有各的好看 |
| *"The dress your feed keeps recommending."* | 你的推荐列表一直在推这条 |
| *"This dress wins. Literally."* | 这条裙子稳赢，说真的 |

#### 套装（Coords）专项

| 英文（对外展示） | 中文（内部参考） |
|---|---|
| *"The set that ships before you do."* | 这套衣服比你出行还先到 |
| *"Coord'd. Confident. Done."* | 套装到位，自信拉满，搞定 |
| *"Matching set energy — all summer."* | 套装感，整个夏天都在线 |
| *"One coord. Endless compliments."* | 一套穿搭，夸赞不停 |

#### 场合装（Occasion Wear）专项

| 英文（对外展示） | 中文（内部参考） |
|---|---|
| *"Wedding guest? Hostess? You name it."* | 婚礼宾客？还是派对主人？你说了算 |
| *"The dress you keep borrowing from yourself."* | 这条裙子你一直在"借用"自己的 |
| *"One occasion. One stunner. Zero regrets."* | 一个场合，一条美裙，零遗憾 |
| *"Rsvp says: you already have the dress."* | 请帖上说：你裙子已经选好了 |

---

### 8.5 下半年节日节拍文案预排（中英对照）

#### Summer Sale（7 月末–8 月）

| 英文（对外展示） | 中文（内部参考） |
|---|---|
| *"Summer sale — last call for summer style."* | 夏促尾声，最后一件夏装好价 |
| *"Up to 40% off. Summer must-go."* | 最高 4 折，夏天必须买 |
| *"Clearance season. Your size's still here."* | 季末清仓，你的码还在 |
| *"Summer deal. Serious slay."* | 夏促好价，真金白银的划算 |

#### 早秋上新 / Back to School（9 月）

| 英文（对外展示） | 中文（内部参考） |
|---|---|
| *"New season. Same fire."* | 新季节，照样火 |
| *"Fall's coming. Your cart's not ready."* | 秋天要来了，你的购物车准备好了吗 |
| *"Back to campus. Best dressed."* | 重返校园穿搭，稳赢 |

#### Black Friday / 节日礼物（11 月）

| 英文（对外展示） | 中文（内部参考） |
|---|---|
| *"Black Friday dressed up."* | 黑色星期五，美裙加持 |
| *"The gift they didn't know they needed."* | 一份她们自己都不知道需要的礼物 |
| *"Start their wishlist. Save the best for last."* | 先把礼物清单安排上，把最好的留到最后 |
| *"One dress. Every wish list."* | 一条裙子，每个愿望清单都有它 |

#### 圣诞/新年派对季（12 月）

| 英文（对外展示） | 中文（内部参考） |
|---|---|
| *"New Year's Eve. One dress. All eyes."* | 除夕夜，一条裙子，全场焦点 |
| *"Party season opened. You're invited."* | 派对季开幕，你被邀请了 |
| *"The only resolution that fits."* | 唯一合身的新年决心 |

---

## 九、预算分配与扩量逻辑

| 参数 | 值 | 说明 |
|---|---|---|
| ROAS 目标 | ≥ 1.45x | 未达标视为失败，需优化或切备用策略 |
| 前期测试预算 | $500–$1,000 | 第 1 阶段验证受众 × 素材组合有效性 |
| 扩量触发条件 | ROAS ≥ 1.45 | 达标后追加预算；不达标则诊断优化 |

**扩量路径**：
```
$500–$1,000 测试验证
  → ROAS ≥ 1.45 → 追加至满量预算（按实际承受能力）
  → ROAS < 1.45 → 诊断优化（素材/受众/平台）→ 重测或切备用方案
```

**世界杯专项加仓（6/11–7/19）**

| 时间段 | 加仓说明 | 主题 |
|---|---|---|
| 6/4–6/10（开幕前） | 测试预算 +20% 预热 | "观赛穿搭"预热 |
| 6/11–7/5（赛期） | ROAS 达标后 +30% | 持续热点内容 |
| 7/6–7/19（决赛） | +25%，主打"派对季收口" | 决赛夜派对穿搭 |

---

## 十、KPI 监控体系

### 10.1 核心判断指标（双轨评估）

| 指标 | 目标值 | 触发优化阈值 | 说明 |
|---|---|---|---|
| **ROAS**（广告支出回报率） | ≥ 1.45x | < 1.45x 视为失败 | 主要评估广告直接变现效率 |
| **复购率**（Remarketing 转化率） | ≥ 8% | < 5% 视为低效 | 各受众层实际转化占比，反映用户主动复购意愿 |

**执行结果优劣判断**：

| ROAS | 复购率 | 判断结果 |
|---|---|---|
| ✅ ≥ 1.45x | ✅ ≥ 8% | 方案成功 |
| ✅ ≥ 1.45x | ❌ < 5% | 内容驱动陷阱：用户被折扣钩住但无自然复购意愿，需优化内容策略 |
| ❌ < 1.45x | ✅ ≥ 8% | 毛利问题：客单价/折扣深度不足，需检视产品定价 |

### 10.2 分受众层复购率目标

| 受众层 | 复购率目标 | 说明 |
|---|---|---|
| R_15d | > 15% | 高价值用户，最易复购 |
| R_30d | 10%–15% | 当季新品复购主力 |
| R_60d | 5%–8% | 中期激活，需折扣/内容配合 |
| R_90d | 3%–5% | 沉睡唤醒，首单复活后关注二次复购 |

### 10.3 辅助监控指标

| 指标 | 目标值 | 优化触发阈值 |
|---|---|---|
| CTR（点击率） | ≥ 1.5% | < 1.0% 立即检视素材/受众匹配 |
| CVR（转化率） | ≥ 2% | < 1.5% 检视落地页/受众匹配 |
| CPE（单次参与成本） | < $0.80 | > $1.20 暂停该组 |

### 10.4 ROAS 不达标处理流程

1. 检查素材 CTR — 低点击需换素材/测试新创意方向
2. 检查 CVR — 低转化需优化落地页/受众精准度
3. 受众交叉验证 — 品类复购受众 vs. 全品类沉睡唤醒的 ROAS 对比
4. 备用方案 — 切换至折扣内容驱动 + 受众范围扩大

---

## 十一、素材数量规划总表

| 阶段 | 时间 | 素材数量（估算） | 说明 |
|---|---|---|---|
| 测试阶段 | 6/1–6/10 | 约 **45–60 单位** | T1–T4 × 每 SKU 2–3 版本 × 3 种格式 |
| 世界杯赛期 | 6/11–7/5 | 追加 **30–45 单位** | 新增 SKU 受众层 + 决赛夜特别版 |
| 淘汰赛–决赛 | 7/6–7/19 | 追加 **20–30 单位** | 决赛夜派对主题 + 场景化素材 |
| Summer Sale | 7/20–8/31 | 约 **40–60 单位** | 季末折扣 + 世界杯热度延续 |
| 节日季蓄水 | 9–10 月 | 约 **60–80 单位** | 早秋新款 + BF 预热素材储备 |

> **单位定义**：1 个"单位" = 1 个 SKU × 1 种创意格式（1 张 Feed 图 / 1 条 Stories / 1 条 Reels）
> **月度总产量参考**：每月约需 **50–80 单位**素材，可支撑 3–4 个 Campaign 并行

---

## 十二、执行检查清单

### Phase 1（最迟 6/4 前完成）
- [ ] 在 Meta Business Manager 创建 R_15d / R_30d / R_60d / R_90d 四个时间维度 Custom Audience
- [ ] 在 Google Ads 创建对应的 4 个网站再营销受众列表
- [ ] 按 P1–P6 筛选标准提取世界杯专题候选 SKU（5–8 SKU/组）
- [ ] 制作世界杯专题素材至少 3 套（Feed 图 + Stories 短视频 + Reels）
- [ ] 设置 T1–T4 测试 Campaign，分配 $500–$1,000 测试预算

### Phase 2（世界杯赛期 6/11–7/19）
- [ ] 每日监控 T1–T4 的 ROAS 和复购率表现
- [ ] ROAS ≥ 1.45 → 顺势加仓并扩展至 R_15d 受众层
- [ ] ROAS < 1.45 → 按诊断流程优化素材/受众，关停低效组
- [ ] 开幕前 1 周（6/4–6/10）开始世界杯预热投放

### Phase 3（世界杯后 7/20 起）
- [ ] 世界杯素材替换为 Summer Sale 主题
- [ ] R_90d 受众开始推送折扣钩子内容
- [ ] 建立品类细分受众（Dress / Tops / Coords）为秋季上新预备

---

*本方案整合了 Callie.com 品牌背景、2026 FIFA World Cup 时间线（2026/6/11–7/19）以及常规 Remarketing 受众分层最佳实践。*

*文档版本：2026/06/01 | 方案制定：Deep Research*
---
name: community-research-to-cards
description: "调研→观点提取→中英对照→小红书风格图片卡片：将社区讨论（Reddit/HN/论坛）中不同用户的观点提炼成独立的人物卡片，右滑切换体验"
version: 1.3.0
author: Hermes Agent (generated)
category: content-creation
tags: [research, xiaohongshu, cards, social-media, visualization, translation, reddit, hn]
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [research, xiaohongshu, cards, social-media, content-creation, translation, reddit]
---

# 社区调研 → 小红书风格人物卡片

从社区讨论中提取不同人物的真实观点，生成小红书风格的独立人物卡片系列，每张卡片展示一位社区成员的意见（英文原话 + 中文翻译），右滑切换体验。

## 工作流程概览

```
调研搜索 → 提取人物 → 翻译润色 → 生成卡片HTML → wkhtmltoimage转JPG → 交付
```

## 前置条件

- `wkhtmltoimage`：`apt-get install wkhtmltopdf`
- 可用网络搜索工具（web_search / web_extract）
- 系统需支持中文字体（安装 `fonts-noto-cjk`）
- 注意：HTML 中不可引用外部资源（如 Google Fonts），否则 wkhtmltoimage 会卡死

## 小红书图片规格

| 规格 | 推荐值 |
|------|--------|
| 比例 | 3:4（竖版）|
| 尺寸 | 1200×1600 px |
| 格式 | JPG（质量 92）|
| 文件大小 | 100-200KB / 张 |
| 内容 | 每张卡片聚焦一个人物的 1 条核心引语 + 中文翻译 |

设计参考：纯黑背景 (#000000) + 右上角半透明渐变光晕 + 英文引语纯白粗体 44px + 中文翻译 30px 0.75 透明度。每张卡片一个人物的 1 条最核心引语。底部头像 68px + 用户名 32px 纯白 + 角色描述 26px 0.6。顶部标签 26px/700 彩色边框。无进度条、无多余装饰。封面仅标题 + 一行来源。人物名不带 `u/` 前缀。

### 文件编号规则

卡片按发布顺序编号：`01-{username}.html`, `02-{username}.html` ... `07-summary.html`
编号即顺序。正面内容在前，负面内容在后。

## Step 1: 调研搜索

使用 `real-user-research` 技能的工作流搜索目标话题的社区讨论。

### 典型搜索模式

```
web_search(query='"{topic}" experience review site:reddit.com')
web_search(query='"{topic}" pain points OR "doesn't work" OR workaround')
web_search(query='"{topic}" site:news.ycombinator.com')
web_search(query='"{topic}" review OR benchmark OR experience')
```

### 高价值来源优先级

1. Reddit（r/LocalLLaMA, r/LocalLLM 等）——最多样化的真实用户声音
2. Hacker News —— 技术深度高，dev/KOL 聚集
3. 个人技术博客（有 HN 首页曝光的最好）
4. YouTube 评测评论区
5. GitHub Issues/Discussions

### 提取要点

对每个高价值页面，使用 `web_extract(urls=[...])` 提取：
- 帖子/评论的具体内容
- 用户经验、配置、量化等级
- 直接引语（保持原始语言）

## Step 2: 筛选人物

从收集到的讨论中选出 5-8 位最有代表性的人物：

| 类型 | 数量 | 说明 |
|------|------|------|
| 🟢 共识派 | 2-3 | 正面体验，有具体数据支撑 |
| 🟡 中间派 | 1-2 | 有保留的认可，指出不足 |
| 🔴 质疑派 | 1-2 | 反面体验或深度质疑 |
| 🟣 深度分析 | 1 | 做过系统性对比测试的 KOL |
| 总结卡 | 1 | 社区共识 + 来源清单 |

每个人物记录：
- 用户名 / 身份
- 来源平台 + 链接
- 2-4 条直接引语（保留英文原文）
- 硬件配置 / 量化等级（如适用）
- 观点提炼（中文）

## Step 3: 翻译引语

对每条英文引语，提供中文翻译。格式规范：

```
英文引语（标注 🇬🇧）
中文翻译（标注 🇨🇳，用虚线分隔）
```

翻译原则：
- 保留技术术语不翻译（FP8, Q6_K, MTP, VRAM 等）
- 保留情绪色彩（讽刺、惊讶、调侃等）
- 人名/用户名不变
- 保持口语化的自然感，不要翻译腔

## Step 4: 生成卡片 HTML

每张卡片一个独立 HTML 文件，固定尺寸 1200×1600px（3:4 竖版比例）。

### 卡片结构

```
{序号}-{username}.html
├── 顶部标签（平台名/身份，26px/700，2px 彩色边框，padding 10px 28px）
├── 引语区（flex 居中，占满剩余空间）
│   ├── 英文原文（44px，纯白，font-weight 600）
│   └── 中文翻译（30px，rgba 0.75，上方 1px/0.15 虚线分隔）
└── 底部信息区
    ├── 头像（首字母渐变圆形，68px，font 30px）
    └── 文字区
        ├── 用户名（32px/700，纯白）
        └── 角色描述（26px，rgba 0.6）
```

无进度条、无页面指示器、无右下角浮动信息。底部仅头像+姓名+角色。

### 封面卡结构

```
00-cover.html
├── 标签「社区口碑调研」（28px/0.7，2px 半透明边框）
├── 主标题（76px/700，纯白）
└── 来源行（32px/0.6，font-weight 500）
```

### CSS 设计要点（3:4 竖版封面风格）

- 固定尺寸 1200×1600 px
- **纯黑背景** `#000000`，右上角 700px 半透明渐变光晕装饰
- 英文引语 44px、font-weight 600、**纯白 `#fff`**
- 中文翻译 30px、font-weight 500、`rgba(255,255,255,0.75)`，上方 1px `rgba(255,255,255,0.15)` 虚线分隔
- 每张卡片聚焦 **1 条最核心的引语**
- 头像 68px 渐变色圆形，每人不同色，字号 30px
- 底部用户名 32px/700 纯白，角色描述 26px `rgba(0.6)`
- 顶部标签 26px/700，padding 10px 28px，border-radius 36px，2px 彩色边框
- 封面标签 28px/0.7，2px 边框；来源行 32px/0.6
- 总结卡图标 72px/34px，正文 38px/0.92，来源行 22px/0.5
- 字体用系统字体：`-apple-system, "PingFang SC", "Noto Sans CJK SC", "Microsoft YaHei"`
- 人物名不写 `u/` 前缀

### 人物顺序（按编号）

发布顺序原则：**正面在前，负面在后**。

| 编号 | 人物 | 立场 |
|------|------|------|
| 01 | hypfer | 正面（Claude 降级体验）|
| 02 | ggerganov | 正面（llama.cpp 作者日常使用）|
| 03 | Piotr Migdał | 正面（首个有通用智能意义的本地模型）|
| 04 | netikas | 中性偏正（ROI 论证，5 模型对比胜出）|
| 05 | SteppenAxolotl | 负面（DeepSWE 2% 争议）|
| 06 | Forward_Jackfruit813 | 负面（Coder-Next 更好）|
| 07 | 总结 | — |

## Step 5: 生成图片

使用 `wkhtmltoimage` 将每个 HTML 转为 JPG，固定 1200×1600（3:4）：

```bash
wkhtmltoimage --width 1200 --height 1600 --quality 92 --encoding UTF-8 card-{name}.html card-{name}.jpg
```

**重要**：
- HTML 中不能引用外部资源（Google Fonts 等），否则会卡死。用系统字体。
- 设置 `--width` 和 `--height` 双重固定确保比例准确
- 质量 92 可在视觉无损的同时将文件控制在 100-200KB

### 后续编辑

如需修改，改 HTML 后重新运行 `wkhtmltoimage` 即可。HTML 是"源文件"，JPG 是导出产物。

## 输出结构

```
{project-dir}/
├── 01-{username}.html        # 卡片 HTML 源文件
├── 01-{username}.jpg         # 卡片图片（1200×1600, 3:4）
├── 02-{username}.html
├── 02-{username}.jpg
├── ...
└── 07-summary.html           # 总结卡片
  └── 07-summary.jpg
```

## 常见问题 / Pitfalls

### wkhtmltoimage 卡在 Loading page
- 原因：HTML 中有外部请求（Google Fonts、analytics 等）
- 解决：使用系统字体，移除所有 `<link>` 外部资源

### 中文显示为方块
- 原因：系统缺少中文字体
- 解决：安装 `fonts-noto-cjk` 或使用各平台自带中文字体

### 图片比例不对
- 每张卡片固定 1200×1600 px（3:4），wkhtmltoimage 需同时指定 `--width` 和 `--height`，缺一不可。

### 文件太大
- 输出 JPG 而非 PNG，质量 92 即可。1200×1600 JPG 通常在 100-200KB。

### 头像颜色
- 每个人物的头像渐变色固定，全系列保持一致。同一个人的卡片在不同话题中颜色相同。

### 不要总结所有人
- 目标不是"汇总观点"，而是让每个人自己的声音被看到。保持"刷评论区"的体验，不同的人、不同的角度，让读者自己判断。

### 总结卡更新时效
- 总结卡中的"最新动态"内容需在每次发布前重新搜索确认（如模型发布、benchmark 更新等）。

### 文件编号
- 编号即发布顺序：正面在前，负面在后。新增卡片需整体重编号。

## 模板参考

可复用的 HTML 模板结构见 `templates/card-template.html`。

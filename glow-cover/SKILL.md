---
name: glow-cover
description: 用程序渲染（Pillow）生成黑底发光文字风格的技术文章封面图，适用于公众号/博客封面。当用户需要生成封面图、题图、cover 图，尤其是包含 AI 模型名、品牌名等必须保证文字零错误的标题时使用；不要用 AI 绘图生成带文字的封面（文字易错），改用本技能的脚本渲染。
---

# Glow Cover 封面渲染

纯黑背景 + 居中白色文字 + 主标题上下两道水平光束 + 主标题泛光（bloom）。三行结构：kicker（上行小字）、title（主标题加粗发光）、subtitle（下行小字）。

## 使用

运行 `scripts/render_cover.py`：

```bash
python3 scripts/render_cover.py \
  --kicker "国产 NPU 本地部署" \
  --title "Qwopus3.6-27B-Coder" \
  --subtitle "接入 Claude Code" \
  --out 封面.png
```

参数：

- `--title`（必填）：主标题，加粗 + 泛光，是唯一带光束的行
- `--kicker` / `--subtitle`（可选）：常规字重，可单独省略，布局自动调整（纯标题时垂直居中）
- `--out`：输出路径，`.png` 或 `.jpg`
- `--width` / `--height`：默认 2848×1600（16:9），布局全部按比例缩放，可改任意尺寸
- `--no-beam`：关闭光束和背景辉光，只保留文字

## 规则

- 文字由调用方（即你）根据文章内容拟定，脚本逐字渲染——模型名、版本号、品牌名照用户原文传参，不要改写、不要意译。
- 中英混排自动处理（CJK 用 Noto Sans CJK SC，拉丁字符用 Liberation Sans）；文字超宽时自动缩字号到 92% 画布宽度以内。
- 主标题尽量不超过 ~25 个字符，过长会显得字号过小；让用户精简或拆分。
- 渲染后把图读回来肉眼检查一遍（文字是否正确、是否溢出），再交付。
- 环境依赖：Pillow 及以上两个系统字体（沙箱已预装；若迁移环境缺字体，先 `apt install fonts-noto-cjk fonts-liberation2`）。

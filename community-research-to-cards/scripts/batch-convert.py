#!/usr/bin/env python3
"""批量将编号卡片 HTML 转 JPG（1200×1600 3:4 比例）"""
import subprocess, sys, os
from pathlib import Path

DIR = sys.argv[1] if len(sys.argv) > 1 else "."
# 匹配 01-*.html, 02-*.html 等
import re
files = sorted(Path(DIR).glob("[0-9][0-9]-*.html"))
if not files:
    print("❌ 未找到编号卡片 HTML 文件")
    sys.exit(1)

for f in files:
    out = f.with_suffix(".jpg")
    print(f"→ {f.name} → {out.name}", end=" ... ", flush=True)
    r = subprocess.run([
        "wkhtmltoimage",
        "--width", "1200",
        "--height", "1600",
        "--quality", "92",
        "--encoding", "UTF-8",
        str(f), str(out)
    ], capture_output=True, text=True, timeout=60)
    if r.returncode == 0:
        size = os.path.getsize(out)
        print(f"✅ {size//1024}KB")
    else:
        print(f"❌ {r.stderr.strip()}")

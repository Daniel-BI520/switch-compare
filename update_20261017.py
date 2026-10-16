# -*- coding: utf-8 -*-
"""双日更新 20261017: 华为 S5731-S 系列包转发率修正"""
import json

BASE = "/Coze/Drive/友商交换机分析"
JSON_PATH = BASE + "/switch_data_normalized.json"
HTML_PATH = BASE + "/index.html"

# 修正映射: model -> (字段, 旧值, 新值)
FIXES = [
    ("CloudEngine S5731-S32ST4X", "forwarding_rate", "280Mpps", "600Mpps"),
    ("CloudEngine S5731-S48T4X", "forwarding_rate", "280Mpps", "560Mpps"),
    ("CloudEngine S5731-S48P4X", "forwarding_rate", "280Mpps", "560Mpps"),
]
DATE = "2026-10-17"

# 1) 更新 JSON
with open(JSON_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)
switches = data["switches"]

changes = []
for model, field, old, new in FIXES:
    hit = [s for s in switches if s["model"] == model]
    assert len(hit) == 1, f"{model} count={len(hit)}"
    s = hit[0]
    assert s.get(field) == old, f"{model} current {s.get(field)} != {old}"
    s[field] = new
    changes.append([model, field, old, new])

data["update_time"] = DATE
with open(JSON_PATH, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

# 2) 重建 index.html 的 switchData / allSwitches 数组
payload = json.dumps([switches], ensure_ascii=False, separators=(",", ":"))

with open(HTML_PATH, "r", encoding="utf-8") as f:
    html = f.read()

def arrspan(txt, kw):
    i = txt.find(kw)
    j = txt.find("[", i)
    depth = 0
    p = j
    while p < len(txt):
        c = txt[p]
        if c == "[":
            depth += 1
        elif c == "]":
            depth -= 1
            if depth == 0:
                break
        p += 1
    return j, p + 1

for kw in ("const switchData =", "const allSwitches ="):
    sj, se = arrspan(html, kw)
    html = html[:sj] + payload + html[se:]

# 3) 更新展示日期 2026-10-15 -> 2026-10-17
assert "2026-10-15" in html, "old date token not found"
html = html.replace("2026-10-15", "2026-10-17")

with open(HTML_PATH, "w", encoding="utf-8") as f:
    f.write(html)

print("JSON updated OK, update_time=", DATE)
print("changes:", json.dumps(changes, ensure_ascii=False))
print("HTML arrays & date updated.")
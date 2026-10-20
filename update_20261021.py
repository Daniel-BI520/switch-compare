# -*- coding: utf-8 -*-
"""双日更新 20261021: 核心参数优先校验, 命中1款核心参数差异(S6850-56HF), 已按H3C官网CN修正"""
import json

BASE = "/Coze/Drive/友商交换机分析"
JSON_PATH = BASE + "/switch_data_normalized.json"
HTML_PATH = BASE + "/index.html"

OLD_DATE = "2026-10-19"
DATE = "2026-10-21"

# 1) 更新 JSON 中 S6850-56HF 核心参数 + update_time
with open(JSON_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)
switches = data["switches"]
assert data.get("update_time") == OLD_DATE, data.get("update_time")

changed = []
for s in switches:
    if s["model"] == "S6850-56HF" and s["vendor"] == "H3C":
        old_cap = s["switching_capacity"]
        old_fwd = s["forwarding_rate"]
        s["switching_capacity"] = "8Tbps/128Tbps"
        s["forwarding_rate"] = "2400Mpps"
        changed.append((old_cap, old_fwd))

data["update_time"] = DATE
with open(JSON_PATH, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print("changed records:", changed)

# 2) 重建 index.html 的 switchData / allSwitches 数组(与json一致) 并刷新 updateTime
payload = json.dumps([switches], ensure_ascii=False, separators=(",", ":"))

with open(HTML_PATH, "r", encoding="utf-8", errors="replace") as f:
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

if OLD_DATE not in html:
    print("WARN: old date token not found in html")
else:
    html = html.replace(OLD_DATE, DATE)

with open(HTML_PATH, "w", encoding="utf-8", errors="replace") as f:
    f.write(html)

print("JSON updated OK, update_time=", DATE)
print("HTML arrays & updateTime updated. switches=", len(switches))
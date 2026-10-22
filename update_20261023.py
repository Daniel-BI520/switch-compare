# -*- coding: utf-8 -*-
"""双日更新 20261023: 核心参数优先校验, 命中2款H3C热门型号核心参数差异, 已按H3C官网CN修正
S6530X-48X8C 交换容量 4.8T/48T -> 8T/80T
S5130S-48UN6X-EI-G-V2 交换容量 672G/6.72T -> 1.36T/13.6T, 包转发率 107Mpps -> 327/770Mpps
"""
import json, sys

BASE = "/Coze/Drive/友商交换机分析"
JSON_PATH = BASE + "/switch_data_normalized.json"
HTML_PATH = BASE + "/index.html"

OLD_DATE = "2026-10-21"
DATE = "2026-10-23"

with open(JSON_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)
switches = data["switches"]
assert data.get("update_time") == OLD_DATE, data.get("update_time")

# 定义修正: (vendor, model, field, new_value)
fixes = [
    ("H3C", "S6530X-48X8C", "switching_capacity", "8Tbps/80Tbps"),
    ("H3C", "S5130S-48UN6X-EI-G-V2", "switching_capacity", "1.36Tbps/13.6Tbps"),
    ("H3C", "S5130S-48UN6X-EI-G-V2", "forwarding_rate", "327Mpps/770Mpps"),
]

changes = []
for s in switches:
    for (v, m, field, newval) in fixes:
        if s["vendor"] == v and s["model"] == m:
            old = s[field]
            if old != newval:
                changes.append([v, m, field, old, newval, "-", "-"])
                s[field] = newval

data["update_time"] = DATE
with open(JSON_PATH, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("changes:", json.dumps(changes, ensure_ascii=False, indent=1))
print("total changes:", len(changes))

# 重建 index.html switchData/allSwitches + 刷新 updateTime
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
    n = html.count(OLD_DATE)
    html = html.replace(OLD_DATE, DATE)
    print("replaced date tokens:", n)

with open(HTML_PATH, "w", encoding="utf-8", errors="replace") as f:
    f.write(html)

print("JSON updated OK, update_time=", DATE)
print("HTML arrays & updateTime updated. switches=", len(switches))
# 输出 changes 用于后续报告/拷贝
with open(BASE + "/validation_logs/changes_20261023.json", "w", encoding="utf-8") as f:
    json.dump(changes, f, ensure_ascii=False, indent=1)
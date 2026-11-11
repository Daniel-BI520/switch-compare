# -*- coding: utf-8 -*-
"""双日更新 20261112: 核心参数优先校验, 三厂商热门/核心型号全部与官网CN一致, 无参数/新增/下架变更"""
import json, re

BASE = "/Coze/Drive/友商交换机分析"
JSON_PATH = BASE + "/switch_data_normalized.json"
HTML_PATH = BASE + "/index.html"

OLD_DATE = "2026-11-10"
DATE = "2026-11-12"

with open(JSON_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)
switches = data["switches"]
print("json update_time:", data.get("update_time"))
data["update_time"] = DATE
with open(JSON_PATH, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

# rebuild index.html arrays (flat) + updateTime
payload = json.dumps(switches, ensure_ascii=False, separators=(",", ":"))

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

# fix updateTime const (clean stray char if any, set to DATE)
html = re.sub(r'const updateTime = "[^"]*"?;', 'const updateTime = "' + DATE + '";', html)
# fix visible date div (2026-11-06 -> DATE)
html = re.sub(r'数据更新时间：[0-9\-]+', '数据更新时间：' + DATE, html)

with open(HTML_PATH, "w", encoding="utf-8", errors="replace") as f:
    f.write(html)

print("update_time set to", DATE, "| switches =", len(switches))
print("payload bytes =", len(payload), "| html bytes =", len(html))

# verify
h2 = open(HTML_PATH, encoding="utf-8", errors="replace").read()
m = re.search(r'const updateTime = "([^"]*)"', h2)
print("verify updateTime:", m.group(1))
v = re.search(r'数据更新时间：([0-9\-]+)', h2)
print("verify visible:", v.group(1))

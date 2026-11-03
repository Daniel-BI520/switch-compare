# -*- coding: utf-8 -*-
"""双日更新 20261104: 核心参数优先校验, 三厂商热门/核心型号全部与官网CN一致, 无参数/新增/下架变更, 仅刷新update_time"""
import json

BASE = "/Coze/Drive/友商交换机分析"
JSON_PATH = BASE + "/switch_data_normalized.json"
HTML_PATH = BASE + "/index.html"

OLD_DATE = "2026-11-02"
DATE = "2026-11-04"

with open(JSON_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)
switches = data["switches"]
assert data.get("update_time") == OLD_DATE, ("unexpected json update_time", data.get("update_time"))
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

if OLD_DATE not in html:
    print("WARN: old date token not found in html")
else:
    html = html.replace(OLD_DATE, DATE)

with open(HTML_PATH, "w", encoding="utf-8", errors="replace") as f:
    f.write(html)

print("update_time set to", DATE, "| switches =", len(switches))
print("payload bytes =", len(payload), "| html bytes =", len(html))

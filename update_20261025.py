# -*- coding: utf-8 -*-
"""双日更新 20261025: 核心参数优先校验(9款重点型号全部一致), 修复2处锐捷URL质量问题
- RG-S5760C-48GT4XS-X  URL 误指向同系列 RG-S5760C-24SFP8GT8XS-X 页 -> 修正为自家产品页
- RG-S6520-64CQ       URL 指向"接入交换机"系列页 -> 修正为独立产品页
"""
import json, sys

BASE = "/Coze/Drive/友商交换机分析"
JSON_PATH = BASE + "/switch_data_normalized.json"
HTML_PATH = BASE + "/index.html"

OLD_DATE = "2026-10-23"
DATE = "2026-10-25"

with open(JSON_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)
switches = data["switches"]
assert data.get("update_time") == OLD_DATE, data.get("update_time")

# 定义修正: (vendor, model, field, new_value, note)
fixes = [
    ("锐捷", "RG-S5760C-48GT4XS-X", "url",
     "https://www.ruijie.com.cn/cp/jh-yqw-hjjh/RG-S5760C-48GT4XS-X/",
     "旧URL误指向同系列24SFP型号页,修正为自家产品页"),
    ("锐捷", "RG-S6520-64CQ", "url",
     "http://www.ruijie.com.cn/cp/jh-shjzhx-sjzxjr/s652064cq/",
     "旧URL指向接入交换机系列页,修正为独立产品页"),
]

changes = []
for s in switches:
    for (v, m, field, newval, note) in fixes:
        if s["vendor"] == v and s["model"] == m:
            old = s[field]
            if old != newval:
                changes.append([v, m, field, old, newval, "-", note])
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
with open(BASE + "/validation_logs/changes_20261025.json", "w", encoding="utf-8") as f:
    json.dump(changes, f, ensure_ascii=False, indent=1)
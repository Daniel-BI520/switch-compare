# -*- coding: utf-8 -*-
"""双日更新 20261120: 核心参数优先校验17款热门与官网CN一致; URL质量扫描修复26款锐捷型号链接指向错误; RG-S7810C标注退市"""
import json, re

BASE = "/Coze/Drive/友商交换机分析"
JSON_PATH = BASE + "/switch_data_normalized.json"
HTML_PATH = BASE + "/index.html"

DATE = "2026-11-20"
OLD_DATE = "2026-11-18"

# 26项URL修复: model -> 确认的正确官网URL(来源: 官网产品页兄弟链接 / 直接fetch页面标题确认)
URL_FIXES = {
    "RG-S5760C-24GT8XS-X": "https://www.ruijie.com.cn/cp/jh-yqw-hjjh/RG-S5760C-24GT8XS-X/",
    "RG-S5760C-48GT4XS-HP-X": "https://www.ruijie.com.cn/cp/jh-yqw-hjjh/s5760c-48gt4xs-hp-x/",
    "RG-S5760C-48SFP4XS-X": "https://www.ruijie.com.cn/cp/jh-yqw-hjjh/s5760c-48sfp4xs-x/",
    "RG-S5750C-28GT4XS-H": "https://www.ruijie.com.cn/cp/jh-yqw-hjjh/s5750c28g4xh/",
    "RG-S5750C-48SFP4XS-H": "https://www.ruijie.com.cn/cp/jh-yqw-hjjh/s5750c48sfp4xsh/",
    "RG-S6231-48XS8CQ": "https://www.ruijie.com.cn/cp/jh-shjzhx-sjzxjr/s623148xs8cq/",
    "RG-S6231-48XT8CQ": "https://www.ruijie.com.cn/cp/jh-shjzhx-sjzxjr/s623148xt8cq/",
    "RG-S6232-48XS8CQ": "https://www.ruijie.com.cn/cp/jh-shjzhx-sjzxjr/s623248xs8cq/",
    "RG-S6233-48XS8CQ": "https://www.ruijie.com.cn/cp/jh-shjzhx-sjzxjr/6233-48xs8cq/",
    "RG-S5310-24GT4XS-P-E": "https://www.ruijie.com.cn/cp/jh-yqw-jrjh/s531024gt4xspe/",
    "RG-S5310-48GT4XS-E": "https://www.ruijie.com.cn/cp/jh-yqw-jrjh/s531048gt4xse/",
    "RG-S5310-48SFP4XS-E": "https://www.ruijie.com.cn/cp/jh-yqw-jrjh/s531048sfp4xse/",
    "RG-S5300-24GT4XS-E": "https://www.ruijie.com.cn/cp/jh-yqw-jrjh/s530024gt4xse/",
    "RG-S5300-48GT4XS-E": "https://www.ruijie.com.cn/cp/jh-yqw-jrjh/s530048gt4xse/",
    "RG-S2910-24GT4SFP-P-L": "https://www.ruijie.com.cn/cp/jh-zxwljj/s2910l-24gt4sfp-p-l",
    "RG-S2910-24GT4XS-L": "https://www.ruijie.com.cn/cp/jh-zxwljj/s2910l-24gt4xs-l",
    "RG-S2910-24GT4XS-P-L": "https://www.ruijie.com.cn/cp/jh-zxwljj/s2910l-24gt4xs-p-l",
    "RG-S2910-48GT4SFP-L": "https://www.ruijie.com.cn/cp/jh-zxwljj/s2910l-48gt4sfp-l",
    "RG-S2910-48GT4XS-L": "https://www.ruijie.com.cn/cp/jh-zxwljj/s2910l-48gt4xs-l",
    "RG-S2910-24GT4XS-UP-H": "https://www.ruijie.com.cn/cp/jh-yqw-jrjh/s291024gt4xsh/",
    "RG-S6120-20XS4VS2QXS": "https://ruijie.com.cn/cp/jh-yqw-hjjh/s612020xs4vs2qxs/",
    "RG-S6160-48VS8CQ-X": "https://www.ruijie.com.cn/cp/jh-yqw-hjjh/rg-s6160-48vs8cq-x/",
    "RG-S6160-48XMG4VS2CQ-UP-X": "https://www.ruijie.com.cn/cp/jh-yqw-hjjh/rg-s6160-48xmg4vs2cq-uo-x/",
    "RG-S7805C": "https://www.ruijie.com.cn/cp/jh-yqw-hxjh/rgs7805cx/",
    "RG-S7808C": "https://www.ruijie.com.cn/cp/jh-shjzhx-sjzxhx/S7808C/",
    "RG-S7810C": "https://www.ruijie.com.cn/cp/jh-yqw-hxjh/s7810c/",
}

with open(JSON_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)
switches = data["switches"]
print("old update_time:", data.get("update_time"))

applied = []
for s in switches:
    m = s.get("model")
    if m in URL_FIXES:
        old_url = s.get("url")
        new_url = URL_FIXES[m]
        if old_url != new_url:
            s["url"] = new_url
            applied.append((m, old_url, new_url))
    if m == "RG-S7810C":
        # 官网退市公告: 2026-06-30停止下单, 2026-12-31停止生产, 替代RG-S7810C-X
        feats = s.get("features", "")
        if "退市" not in feats:
            s["features"] = (feats + " | 已发布退市公告(2026-06-30停售, 2026-12-31停产), 替代型号RG-S7810C-X").strip(" |")

data["update_time"] = DATE
with open(JSON_PATH, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("URL fixes applied:", len(applied))
for m, old, new in applied:
    print("  ", m, "\n   old:", old, "\n   new:", new)

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

html = re.sub(r'const updateTime = "[^"]*";', 'const updateTime = "' + DATE + '";', html)
html = re.sub(r'数据更新时间：[0-9\-]+', '数据更新时间：' + DATE, html)

with open(HTML_PATH, "w", encoding="utf-8", errors="replace") as f:
    f.write(html)

print("update_time set to", DATE, "| switches =", len(switches))
print("payload bytes =", len(payload), "| html bytes =", len(html))

h2 = open(HTML_PATH, encoding="utf-8", errors="replace").read()
m = re.search(r'const updateTime = "([^"]*)"', h2)
print("verify updateTime:", m.group(1) if m else "NOT_FOUND")
v = re.search(r'数据更新时间：([0-9\-]+)', h2)
print("verify visible:", v.group(1) if v else "NOT_FOUND")

# verify a few URL fixes landed in html
for key in ["rg-s6160-48vs8cq-x", "s612020xs4vs2qxs", "rgs7805cx", "s7810c/"]:
    print("html contains", key, ":", key in h2)
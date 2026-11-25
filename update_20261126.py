# -*- coding: utf-8 -*-
"""双日更新 20261126: 17款热门核心参数(交换容量+包转发率)全部与官网CN一致;
数据规范修正 S6550X-54H-HI 旧字段结构->标准字段结构, 标"新"标签(2026-04-24发布≤12个月);
update_time -> 2026-11-26"""
import json, re

BASE = "/Coze/Drive/友商交换机分析"
JSON_PATH = BASE + "/switch_data_normalized.json"
HTML_PATH = BASE + "/index.html"
DATE = "2026-11-26"

with open(JSON_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)
switches = data["switches"]
print("old update_time:", data.get("update_time"), "| switches:", len(switches))

# 1) S6550X-54H-HI 字段标准化 + 新标签
target = None
for s in switches:
    if s.get("model") == "S6550X-54H-HI":
        target = s
        break
if target is None:
    raise SystemExit("S6550X-54H-HI not found!")

print("before:", json.dumps(target, ensure_ascii=False))
standard = {
    "vendor": "H3C",
    "series": "S6550X-HI系列多通道以太光交换机",
    "model": "S6550X-54H-HI",
    "tier": "汇聚",
    "switching_capacity": "48Tbps",
    "forwarding_rate": "9600Mpps",
    "ports": "54个40G/100G QSFP28端口，2个10G SFP+端口",
    "poe_support": "不支持",
    "expansion_slots": "0",
    "power_redundancy": "2个电源插槽，1+1冗余",
    "fan_redundancy": "6个风扇插槽",
    "url": "https://www.h3c.com/cn/Products_And_Solution/InterConnect/Products/Switches/Products/EPON/All-Optical/Aggregation/S6550X_HI/",
    "features": "多通道以太光方案(1:1无损耗), 54口100GE高密, IRF2堆叠, M-LAG, VXLAN, EVPN, OpenFlow 1.3, PTP, Telemetry",
    "is_hot": bool(target.get("is_hot", False)),
    "is_new": True,
}
switches[switches.index(target)] = standard
print("after:", json.dumps(standard, ensure_ascii=False))

data["update_time"] = DATE
with open(JSON_PATH, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print("JSON updated, update_time =", DATE)

# 2) 同步 index.html
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
print("HTML updated, payload bytes:", len(payload), "| html bytes:", len(html))

# 3) 校验
h2 = open(HTML_PATH, encoding="utf-8", errors="replace").read()
m = re.search(r'const updateTime = "([^"]*)"', h2)
print("verify updateTime:", m.group(1) if m else "NOT_FOUND")
v = re.search(r'数据更新时间：([0-9\-]+)', h2)
print("verify visible:", v.group(1) if v else "NOT_FOUND")
print("html contains S6550X-54H-HI (std fields):", '"tier":"汇聚"' in h2 or '"tier": "汇聚"' in h2)

# 4) 变更清单
changes = {
    "date": "2026-11-26",
    "summary": {"新增": 0, "参数更新": 0, "下架": 0, "URL修复": 0, "数据规范修正": 1},
    "param_updates": [],
    "notes": [
        "17款热门型号核心参数(交换容量+包转发率)全部与官网CN一致",
        "抽查 CE6857F-48S6CQ/S6520X-30QC-EI/RG-S5760C 系列与官网CN一致",
        "S6550X-54H-HI: 旧字段结构(level/poe/extended_slots/release_date)修正为标准结构(tier/poe_support/expansion_slots/power_redundancy/fan_redundancy), 官网2026-04-24发布, 标'新'标签",
        "RG-S6503-48VS8CQ 中文官网无独立产品页(404), 按URL红线不入库",
        "H3C/华为智算互联新品(S9828-64FP/S9828-128EO/S12500R-64EP等)不在入库范围",
    ],
}
with open(BASE + "/validation_logs/changes_20261126.json", "w", encoding="utf-8") as f:
    json.dump(changes, f, ensure_ascii=False, indent=2)
print("changes_20261126.json saved")
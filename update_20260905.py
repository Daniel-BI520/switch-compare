#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
交换机参数双日更新 - 2026-09-05
策略：核心参数优先校验 + 疑点深挖 + 新型号补全
"""

import json
import re
from datetime import datetime
from collections import defaultdict

DATA_FILE = 'switch_data_normalized.json'
HTML_FILE = 'index.html'
CHANGES_FILE = 'validation_logs/changes_20260905.json'
REPORT_FILE = 'validation_logs/update_report_20260905.md'

changes = []

def add_change(vendor, model, param, old, new, reason, source):
    changes.append({
        'vendor': vendor,
        'model': model,
        'param': param,
        'old': old,
        'new': new,
        'reason': reason,
        'source': source
    })

# 1. 读取数据
with open(DATA_FILE, 'r', encoding='utf-8') as f:
    data = json.load(f)
switches = data['switches']
print(f"读取数据完成，共 {len(switches)} 款")

existing_models = {s['model']: s for s in switches}

# ========== 新增1：华为 S5735-L-V2 2.5GE电口PoE系列补全 ==========
new_models_huawei_25ge = [
    {
        'vendor': '华为',
        'series': 'CloudEngine S5735-L-V2系列（2.5GE电口）',
        'model': 'CloudEngine S5735-L24PN4XE-A-V2',
        'tier': '接入',
        'switching_capacity': '672Gbps/6.72Tbps',
        'forwarding_rate': '225Mpps',
        'ports': '24个10/100/1000/2.5G BASE-T PoE+以太网端口，4个万兆SFP+，2个专用堆叠口',
        'poe_support': 'PoE+（400W）',
        'url': 'https://e.huawei.com/cn/products/switches/campus-switches/s5735-l-v2-ge',
        'features': '2.5GE到桌面接入，内置AC供电，支持静态路由/RIP/OSPF三层路由，Telemetry智能运维',
        'expansion_slots': '无',
        'power_redundancy': '不支持（内置AC）',
        'fan_redundancy': '智能调速风扇',
        'is_hot': False,
        'is_new': True,
    },
    {
        'vendor': '华为',
        'series': 'CloudEngine S5735-L-V2系列（2.5GE电口）',
        'model': 'CloudEngine S5735-L48PN4XE-A-V2',
        'tier': '接入',
        'switching_capacity': '672Gbps/6.72Tbps',
        'forwarding_rate': '315Mpps',
        'ports': '48个10/100/1000/2.5G BASE-T PoE+以太网端口，4个万兆SFP+，2个专用堆叠口',
        'poe_support': 'PoE+（828W）',
        'url': 'https://e.huawei.com/cn/products/switches/campus-switches/s5735-l-v2-ge',
        'features': '2.5GE到桌面接入，48口高密度PoE+，内置AC供电，支持静态路由/RIP/OSPF三层路由',
        'expansion_slots': '无',
        'power_redundancy': '不支持（内置AC）',
        'fan_redundancy': '智能调速风扇',
        'is_hot': False,
        'is_new': True,
    },
    {
        'vendor': '华为',
        'series': 'CloudEngine S5735-L-V2系列（2.5GE电口）',
        'model': 'CloudEngine S5735-L48LPN4XE-A-V2',
        'tier': '接入',
        'switching_capacity': '672Gbps/6.72Tbps',
        'forwarding_rate': '315Mpps',
        'ports': '48个10/100/1000/2.5G BASE-T PoE+以太网端口，4个万兆SFP+，2个专用堆叠口',
        'poe_support': 'PoE+（360W，长距PoE）',
        'url': 'https://e.huawei.com/cn/products/switches/campus-switches/s5735-l-v2-ge',
        'features': '2.5GE到桌面长距PoE款，360W低功耗PoE+，内置AC供电，支持静态路由/RIP/OSPF三层路由',
        'expansion_slots': '无',
        'power_redundancy': '不支持（内置AC）',
        'fan_redundancy': '智能调速风扇',
        'is_hot': False,
        'is_new': True,
    },
]

for m in new_models_huawei_25ge:
    if m['model'] not in existing_models:
        switches.append(m)
        existing_models[m['model']] = m
        add_change('华为', m['model'], 'new_model', '', m['model'],
                   '华为S5735-L-V2系列2.5GE电口PoE型号补全，2.5G到桌面场景',
                   'https://e.huawei.com/cn/products/switches/campus-switches/s5735-l-v2-ge')
        print(f"+ 新增 {m['model']}")
    else:
        print(f"! {m['model']} 已存在，跳过")

# ========== 更新update_time ==========
data['update_time'] = '2026-09-05'

# ========== 保存JSON ==========
with open(DATA_FILE, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print(f"\nJSON保存完成，总型号数: {len(switches)}")

# ========== 同步更新index.html ==========
print("\n同步更新index.html...")
with open(HTML_FILE, 'r', encoding='utf-8') as f:
    html_content = f.read()

switches_json = json.dumps(switches, ensure_ascii=False, indent=2)

old_switch_data_pattern = r'(const switchData\s*=\s*)(\[.*?\])(;)'
match = re.search(old_switch_data_pattern, html_content, re.DOTALL)
if match:
    html_content = html_content[:match.start(2)] + switches_json + html_content[match.end(2):]
    print("switchData 变量已更新")
else:
    print("未找到 switchData 变量")

old_all_pattern = r'(const allSwitches\s*=\s*)(\[.*?\])(;)'
match = re.search(old_all_pattern, html_content, re.DOTALL)
if match:
    html_content = html_content[:match.start(2)] + switches_json + html_content[match.end(2):]
    print("allSwitches 变量已更新")
else:
    print("未找到 allSwitches 变量")

with open(HTML_FILE, 'w', encoding='utf-8') as f:
    f.write(html_content)
print("index.html 保存完成")

# ========== 保存变更记录 ==========
with open(CHANGES_FILE, 'w', encoding='utf-8') as f:
    json.dump(changes, f, ensure_ascii=False, indent=2)
print(f"\n变更记录已保存到 {CHANGES_FILE}，共 {len(changes)} 条")

# ========== 统计信息 ==========
vendor_count = defaultdict(int)
tier_count = defaultdict(int)
for s in switches:
    vendor_count[s['vendor']] += 1
    tier_count[s['tier']] += 1

new_count = len([c for c in changes if c['param'] == 'new_model'])
param_fix_count = len([c for c in changes if c['param'] != 'new_model'])
hot_count = len([s for s in switches if s.get('is_hot') and s['vendor'] != '锐捷'])
new_tag_count = len([s for s in switches if s.get('is_new') and s['vendor'] != '锐捷'])
discontinued_count = len([s for s in switches if s.get('discontinued')])
no_url_count = len([s for s in switches if not s.get('url') or s['url'] == ''])

print(f"\n统计: 总{len(switches)}款 | 锐捷{vendor_count['锐捷']} | 华为{vendor_count['华为']} | H3C {vendor_count['H3C']}")
print(f"  新增型号: {new_count}款 | 参数修正: {param_fix_count}处")
print(f"  热门型号: {hot_count}款 | 新型号: {new_tag_count}款")
print(f"  已停产: {discontinued_count}款 | 无URL: {no_url_count}款")

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
交换机参数双日更新 - 2026-08-30
策略：核心参数优先校验 + 疑点深挖
"""

import json
import re
from datetime import datetime

DATA_FILE = 'switch_data_normalized.json'
HTML_FILE = 'index.html'
CHANGES_FILE = 'validation_logs/changes_20260830.json'
REPORT_FILE = 'validation_logs/update_report_20260830.md'

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

# ========== 修正1：华为S5735-L24T4XE-A-V2 核心参数 ==========
# 官网：672Gbps/6.72Tbps, 171Mpps
# 现有：176Gbps/520Gbps, 132Mpps
model = 'S5735-L24T4XE-A-V2'
if model in existing_models:
    s = existing_models[model]
    old_sc = s['switching_capacity']
    old_fr = s['forwarding_rate']
    s['switching_capacity'] = '672Gbps/6.72Tbps'
    s['forwarding_rate'] = '171Mpps'
    # 同步更新端口描述，官网为带堆叠口
    s['ports'] = '24个10/100/1000BASE-T以太网端口，4个万兆SFP+，2个12GE专用堆叠口'
    add_change('华为', model, 'switching_capacity', old_sc, '672Gbps/6.72Tbps',
               '核心参数修正，旧版数据为176G/520G，官网最新为672G/6.72T',
               'https://e.huawei.com/cn/products/switches/campus-switches/s5735-l-v2')
    add_change('华为', model, 'forwarding_rate', old_fr, '171Mpps',
               '核心参数修正，旧版132Mpps，官网最新171Mpps',
               'https://e.huawei.com/cn/products/switches/campus-switches/s5735-l-v2')
    print(f"✅ 修正 {model}: 交换容量 {old_sc}→672Gbps/6.72Tbps, 包转发率 {old_fr}→171Mpps")

# ========== 修正2：华为S5735-L48T4XE-A-V2 核心参数 ==========
model = 'S5735-L48T4XE-A-V2'
if model in existing_models:
    s = existing_models[model]
    old_sc = s['switching_capacity']
    old_fr = s['forwarding_rate']
    s['switching_capacity'] = '672Gbps/6.72Tbps'
    s['forwarding_rate'] = '207Mpps'
    s['ports'] = '48个10/100/1000BASE-T以太网端口，4个万兆SFP+，2个12GE专用堆叠口'
    add_change('华为', model, 'switching_capacity', old_sc, '672Gbps/6.72Tbps',
               '核心参数修正，旧版数据为224G/520G，官网最新为672G/6.72T',
               'https://e.huawei.com/cn/products/switches/campus-switches/s5735-l-v2')
    add_change('华为', model, 'forwarding_rate', old_fr, '207Mpps',
               '核心参数修正，旧版168Mpps，官网最新207Mpps',
               'https://e.huawei.com/cn/products/switches/campus-switches/s5735-l-v2')
    print(f"✅ 修正 {model}: 交换容量 {old_sc}→672Gbps/6.72Tbps, 包转发率 {old_fr}→207Mpps")

# ========== 新增1：华为S5735-S-V2 8J光电分离系列 + XA系列 ==========
new_models_huawei_s = [
    # S48T4XE-XA-V2: 内置双AC电源，1+1备份，无扩展槽
    {
        'vendor': '华为',
        'series': 'CloudEngine S5735-S-V2系列',
        'model': 'CloudEngine S5735-S48T4XE-XA-V2',
        'tier': '接入',
        'switching_capacity': '1.36Tbps/13.6Tbps',
        'forwarding_rate': '327Mpps/770Mpps',
        'ports': '48个10/100/1000BASE-T以太网端口，4个万兆SFP+，2个专用堆叠口',
        'poe_support': '不支持',
        'url': 'https://e.huawei.com/cn/products/switches/campus-switches/s5735-s-v2',
        'features': '内置双AC供电，支持1+1备份，无扩展插槽，支持静态路由/RIP/OSPF/BGP/VRRP等三层路由',
        'expansion_slots': '无',
        'power_redundancy': '内置双AC，1+1备份',
        'fan_redundancy': '智能调速风扇',
        'is_hot': False,
        'is_new': True,
    },
    # S24T8J4XE-XA-V2: 2.5GE光电分离，内置双AC
    {
        'vendor': '华为',
        'series': 'CloudEngine S5735-S-V2系列',
        'model': 'CloudEngine S5735-S24T8J4XE-XA-V2',
        'tier': '接入',
        'switching_capacity': '1.36Tbps/13.6Tbps',
        'forwarding_rate': '321Mpps/770Mpps',
        'ports': '24个10/100/1000BASE-T以太网端口，8个2.5GE SFP(可切换为2个10GE SFP+)，4个10GE SFP+，2个专用堆叠口',
        'poe_support': '不支持',
        'url': 'https://e.huawei.com/cn/products/switches/campus-switches/s5735-s-v2',
        'features': '2.5GE光电分离灵活光口，内置双AC供电1+1备份，支持静态路由/RIP/OSPF/BGP/VRRP',
        'expansion_slots': '无',
        'power_redundancy': '内置双AC，1+1备份',
        'fan_redundancy': '智能调速风扇',
        'is_hot': False,
        'is_new': True,
    },
    # S24T8J4XEZ-V2: 2.5GE光电分离，Z版本带扩展槽
    {
        'vendor': '华为',
        'series': 'CloudEngine S5735-S-V2系列',
        'model': 'CloudEngine S5735-S24T8J4XEZ-V2',
        'tier': '接入',
        'switching_capacity': '1.36Tbps/13.6Tbps',
        'forwarding_rate': '321Mpps/770Mpps',
        'ports': '24个10/100/1000BASE-T以太网端口，8个2.5GE SFP(可切换为2个10GE SFP+)，4个10GE SFP+，2个专用堆叠口',
        'poe_support': '不支持',
        'url': 'https://e.huawei.com/cn/products/switches/campus-switches/s5735-s-v2',
        'features': '2.5GE光电分离灵活光口，预留后插卡槽位，1+1电源备份，支持静态路由/RIP/OSPF/BGP/VRRP',
        'expansion_slots': '预留后插卡槽位',
        'power_redundancy': '1+1电源备份',
        'fan_redundancy': '智能调速风扇',
        'is_hot': False,
        'is_new': True,
    },
    # S24P8J4XEZ-V2: 2.5GE光电分离PoE+，Z版本带扩展槽
    {
        'vendor': '华为',
        'series': 'CloudEngine S5735-S-V2系列',
        'model': 'CloudEngine S5735-S24P8J4XEZ-V2',
        'tier': '接入',
        'switching_capacity': '1.36Tbps/13.6Tbps',
        'forwarding_rate': '321Mpps/770Mpps',
        'ports': '24个10/100/1000BASE-T PoE+以太网端口，8个2.5GE SFP(可切换为2个10GE SFP+)，4个10GE SFP+，2个专用堆叠口',
        'poe_support': 'PoE+',
        'url': 'https://e.huawei.com/cn/products/switches/campus-switches/s5735-s-v2',
        'features': '2.5GE光电分离灵活光口，PoE+供电，预留后插卡槽位，3电源N+1备份',
        'expansion_slots': '预留后插卡槽位',
        'power_redundancy': '3电源，N+1电源备份',
        'fan_redundancy': '智能调速风扇',
        'is_hot': False,
        'is_new': True,
    },
]

for m in new_models_huawei_s:
    if m['model'] not in existing_models:
        switches.append(m)
        existing_models[m['model']] = m
        add_change('华为', m['model'], 'new_model', '', m['model'],
                   '华为S5735-S-V2系列光电分离8J型号补全，2.5GE灵活光口设计',
                   'https://e.huawei.com/cn/products/switches/campus-switches/s5735-s-v2')
        print(f"➕ 新增 {m['model']}")
    else:
        print(f"⚠️  {m['model']} 已存在，跳过")

# ========== 新增2：华为S5735-L24T8J4XE-A-V2 2.5GE光电分离 ==========
new_model_l = {
    'vendor': '华为',
    'series': 'CloudEngine S5735-L-V2系列',
    'model': 'CloudEngine S5735-L24T8J4XE-A-V2',
    'tier': '接入',
    'switching_capacity': '672Gbps/6.72Tbps',
    'forwarding_rate': '201Mpps',
    'ports': '24个10/100/1000BASE-T以太网端口，8个2.5GE SFP(可切换为2个10GE SFP+)，4个10GE SFP+，2个专用堆叠口',
    'poe_support': '不支持',
    'url': 'https://e.huawei.com/cn/products/switches/campus-switches/s5735-l-v2',
    'features': '2.5GE光电分离灵活光口，支持静态路由/RIP/OSPF三层路由，Telemetry智能运维',
    'expansion_slots': '无',
    'power_redundancy': '不支持',
    'fan_redundancy': '智能调速风扇',
    'is_hot': False,
    'is_new': True,
}

if new_model_l['model'] not in existing_models:
    switches.append(new_model_l)
    existing_models[new_model_l['model']] = new_model_l
    add_change('华为', new_model_l['model'], 'new_model', '', new_model_l['model'],
               '华为S5735-L-V2系列2.5GE光电分离型号新增，8个2.5GE SFP灵活光口',
               'https://e.huawei.com/cn/products/switches/campus-switches/s5735-l-v2')
    print(f"➕ 新增 {new_model_l['model']}")

# ========== 更新update_time ==========
data['update_time'] = '2026-08-30'

# ========== 保存JSON ==========
with open(DATA_FILE, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print(f"\n💾 JSON保存完成，总型号数: {len(switches)}")

# ========== 同步更新index.html ==========
print("\n🔄 同步更新index.html...")
with open(HTML_FILE, 'r', encoding='utf-8') as f:
    html_content = f.read()

# 构造switchData变量
switches_json = json.dumps(switches, ensure_ascii=False, indent=2)

# 替换 switchData 变量
old_switch_data_pattern = r'(const switchData\s*=\s*)(\[.*?\])(;)'
match = re.search(old_switch_data_pattern, html_content, re.DOTALL)
if match:
    html_content = html_content[:match.start(2)] + switches_json + html_content[match.end(2):]
    print("✅ switchData 变量已更新")
else:
    print("⚠️  未找到 switchData 变量")

# 替换 allSwitches 变量
old_all_pattern = r'(const allSwitches\s*=\s*)(\[.*?\])(;)'
match = re.search(old_all_pattern, html_content, re.DOTALL)
if match:
    html_content = html_content[:match.start(2)] + switches_json + html_content[match.end(2):]
    print("✅ allSwitches 变量已更新")
else:
    print("⚠️  未找到 allSwitches 变量")

with open(HTML_FILE, 'w', encoding='utf-8') as f:
    f.write(html_content)
print("💾 index.html 保存完成")

# ========== 保存变更记录 ==========
with open(CHANGES_FILE, 'w', encoding='utf-8') as f:
    json.dump(changes, f, ensure_ascii=False, indent=2)
print(f"\n📋 变更记录已保存到 {CHANGES_FILE}，共 {len(changes)} 条")

# ========== 统计信息 ==========
from collections import defaultdict
vendor_count = defaultdict(int)
for s in switches:
    vendor_count[s['vendor']] += 1

new_count = len([c for c in changes if c['param'] == 'new_model'])
param_fix_count = len([c for c in changes if c['param'] != 'new_model'])
hot_count = len([s for s in switches if s.get('is_hot') and s['vendor'] != '锐捷'])
new_tag_count = len([s for s in switches if s.get('is_new') and s['vendor'] != '锐捷'])

print(f"\n📊 统计: 总{len(switches)}款 | 锐捷{vendor_count['锐捷']} | 华为{vendor_count['华为']} | H3C {vendor_count['H3C']}")
print(f"   新增型号: {new_count}款 | 参数修正: {param_fix_count}处")


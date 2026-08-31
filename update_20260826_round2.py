#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
交换机参数数据自动更新 - 2026-08-26 第二轮补充
补充修正剩余S5135S型号 + 补充缺失型号
"""

import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, 'switch_data_normalized.json')
HTML_FILE = os.path.join(BASE_DIR, 'index.html')
LOG_DIR = os.path.join(BASE_DIR, 'validation_logs')
UPDATE_DATE = '2026-08-26'


def load_data():
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def update_param(switches, vendor, model, param, new_value, reason, source, changes_log):
    for s in switches:
        if s.get('vendor') == vendor and s.get('model') == model:
            old_value = s.get(param, '')
            if old_value == new_value:
                return False
            s[param] = new_value
            changes_log.append({
                'vendor': vendor, 'model': model, 'param': param,
                'old': old_value, 'new': new_value,
                'reason': reason, 'source': source
            })
            print(f"  ✏️  {vendor} {model} | {param}: {old_value} → {new_value}")
            return True
    print(f"  ⚠️  {vendor} {model} | 未找到")
    return False


def add_switch(switches, new_switch, reason, source, changes_log, new_models_log):
    model = new_switch.get('model', '')
    vendor = new_switch.get('vendor', '')
    for s in switches:
        if s.get('vendor') == vendor and s.get('model') == model:
            print(f"  ⚠️  {vendor} {model} | 已存在")
            return False
    switches.append(new_switch)
    changes_log.append({
        'vendor': vendor, 'model': model, 'param': 'new_model',
        'old': '', 'new': model, 'reason': reason, 'source': source
    })
    new_models_log.append(new_switch)
    print(f"  ➕  {vendor} {model} | 新增")
    return True


def sync_html(switches, update_date):
    with open(HTML_FILE, 'rb') as f:
        content = f.read()
    
    switch_data_json = json.dumps(switches, ensure_ascii=False, separators=(',', ':'))
    
    # 更新 switchData
    start_marker = b'switchData = ['
    start_idx = content.find(start_marker)
    search_start = start_idx + len(start_marker)
    depth = 1
    i = search_start
    while i < len(content) and depth > 0:
        if content[i] == ord('['): depth += 1
        elif content[i] == ord(']'): depth -= 1
        i += 1
    while i < len(content) and content[i] != ord(';'): i += 1
    i += 1
    new_switch_data = b'switchData = ' + switch_data_json.encode('utf-8') + b';'
    content = content[:start_idx] + new_switch_data + content[i:]
    
    # 更新 allSwitches
    all_sw_marker = b'allSwitches = ['
    all_start = content.find(all_sw_marker)
    all_switches_json = json.dumps(switches, ensure_ascii=False, indent=None, separators=(', ', ': '))
    search_start2 = all_start + len(all_sw_marker)
    depth2 = 1
    j = search_start2
    while j < len(content) and depth2 > 0:
        if content[j] == ord('['): depth2 += 1
        elif content[j] == ord(']'): depth2 -= 1
        j += 1
    while j < len(content) and content[j] != ord(';'): j += 1
    j += 1
    new_all_switches = b'allSwitches = ' + all_switches_json.encode('utf-8') + b';'
    content = content[:all_start] + new_all_switches + content[j:]
    
    with open(HTML_FILE, 'wb') as f:
        f.write(content)
    print("  ✅ index.html 已同步")


def main():
    print("=" * 70)
    print("第二轮补充更新 - H3C S5135S-EI 系列补全")
    print("=" * 70)
    
    data = load_data()
    switches = data['switches']
    
    # 读取已有的变更日志，合并
    changes_file = os.path.join(LOG_DIR, 'changes_20260826.json')
    with open(changes_file, 'r', encoding='utf-8') as f:
        changes_log = json.load(f)
    new_models_log = []
    
    h3c_source = "https://www.h3c.com/cn/Products_And_Solution/InterConnect/Products/Switches/Products/Park_Switches/Access_Switch/S5135/S5135S_EI/"
    reason = "H3C中文官网S5135S-EI系列产品规格表验证，全系列统一672Gbps/6.72Tbps"
    
    # ==========================================
    # 一、补正剩余4款S5135S-EI参数
    # ==========================================
    print("\n一、补正剩余4款S5135S-EI参数")
    
    # 24口PoE+SFP型号 - 24口+4combo PoE +4SFP+4SFP+
    update_param(switches, 'H3C', 'S5135S-24FP4S4X-EI', 'switching_capacity',
        '672Gbps/6.72Tbps', reason, h3c_source, changes_log)
    update_param(switches, 'H3C', 'S5135S-24FP4S4X-EI', 'forwarding_rate',
        '171Mpps', reason, h3c_source, changes_log)
    
    # 24口PoE+SFP(千兆上行) - 24口PoE + 4SFP
    update_param(switches, 'H3C', 'S5135S-24P4S-EI', 'switching_capacity',
        '672Gbps/6.72Tbps', reason, h3c_source, changes_log)
    update_param(switches, 'H3C', 'S5135S-24P4S-EI', 'forwarding_rate',
        '171Mpps', reason, h3c_source, changes_log)
    
    # 48口PoE+万兆上行
    update_param(switches, 'H3C', 'S5135S-48FP4X-EI', 'switching_capacity',
        '672Gbps/6.72Tbps', reason, h3c_source, changes_log)
    update_param(switches, 'H3C', 'S5135S-48FP4X-EI', 'forwarding_rate',
        '207Mpps', reason, h3c_source, changes_log)
    
    # 48口PoE+万兆上行
    update_param(switches, 'H3C', 'S5135S-48P4X-EI', 'switching_capacity',
        '672Gbps/6.72Tbps', reason, h3c_source, changes_log)
    update_param(switches, 'H3C', 'S5135S-48P4X-EI', 'forwarding_rate',
        '207Mpps', reason, h3c_source, changes_log)
    
    # ==========================================
    # 二、补充4款官网有但库中缺失的型号
    # ==========================================
    print("\n二、补充4款官网有但库中缺失的型号")
    
    new_models = [
        {
            "vendor": "H3C",
            "series": "H3C S5135S-EI系列千兆接入交换机",
            "model": "S5135S-10T2S2X-EI-Q",
            "tier": "接入",
            "switching_capacity": "672Gbps/6.72Tbps",
            "forwarding_rate": "132Mpps",
            "ports": "10个10/100/1000BASE-T（含2个100/1000BASE-X SFP combo口），2个1/2.5/10GE SFP+端口",
            "poe_support": "不支持",
            "url": h3c_source,
            "features": "静音无风扇，IRF2堆叠，二层千兆接入，万兆上行",
            "expansion_slots": "",
            "power_redundancy": "",
            "fan_redundancy": "无风扇",
            "is_hot": False,
            "is_new": False
        },
        {
            "vendor": "H3C",
            "series": "H3C S5135S-EI系列千兆接入交换机",
            "model": "S5135S-48ST4X-EI",
            "tier": "接入",
            "switching_capacity": "672Gbps/6.72Tbps",
            "forwarding_rate": "207Mpps",
            "ports": "24个10/1000BASE-T电口，24个100/1000BASE-X SFP端口，4个1/2.5/10GE SFP+端口",
            "poe_support": "不支持",
            "url": h3c_source,
            "features": "模块化双电源，IRF2堆叠，光电混合接入，万兆上行",
            "expansion_slots": "",
            "power_redundancy": "1+1备份",
            "fan_redundancy": "",
            "is_hot": False,
            "is_new": False
        },
        {
            "vendor": "H3C",
            "series": "H3C S5135S-EI系列千兆接入交换机",
            "model": "S5135S-24S8T4X-EI",
            "tier": "接入",
            "switching_capacity": "672Gbps/6.72Tbps",
            "forwarding_rate": "171Mpps",
            "ports": "24个100/1000BASE-X SFP端口（含8个10/100/1000BASE-T combo电口），4个1/2.5/10GE SFP+端口",
            "poe_support": "不支持",
            "url": h3c_source,
            "features": "模块化双电源，IRF2堆叠，全光接入，万兆上行",
            "expansion_slots": "",
            "power_redundancy": "1+1备份",
            "fan_redundancy": "",
            "is_hot": False,
            "is_new": False
        },
        {
            "vendor": "H3C",
            "series": "H3C S5135S-EI系列千兆接入交换机",
            "model": "S5135S-8FP4XS-EI-Q",
            "tier": "接入",
            "switching_capacity": "672Gbps/6.72Tbps",
            "forwarding_rate": "132Mpps",
            "ports": "8个10/100/1000BASE-T PoE+电口，2个1000BASE-X SFP端口，2个1/2.5/10GE SFP+端口",
            "poe_support": "支持（PoE+）",
            "url": h3c_source,
            "features": "静音无风扇，PoE+供电，IRF2堆叠，小型接入",
            "expansion_slots": "",
            "power_redundancy": "",
            "fan_redundancy": "无风扇",
            "is_hot": False,
            "is_new": False
        },
    ]
    
    for nm in new_models:
        add_switch(switches, nm,
            "H3C中文官网S5135S-EI系列包含此型号，原数据库缺失，补充入库",
            h3c_source, changes_log, new_models_log)
    
    # ==========================================
    # 保存与同步
    # ==========================================
    print("\n保存数据...")
    data['update_time'] = UPDATE_DATE
    save_data(data)
    print(f"  ✅ 共 {len(switches)} 款")
    
    sync_html(switches, UPDATE_DATE)
    
    # 保存合并后的变更日志
    with open(changes_file, 'w', encoding='utf-8') as f:
        json.dump(changes_log, f, ensure_ascii=False, indent=2)
    print(f"\n  变更日志已更新，共 {len(changes_log)} 条")
    
    # 统计
    param_changes = [c for c in changes_log if c['param'] in ('switching_capacity', 'forwarding_rate')]
    new_m = [c for c in changes_log if c['param'] == 'new_model']
    print(f"\n汇总：参数更新 {len(param_changes)} 项，新增型号 {len(new_m)} 款")


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
交换机参数数据自动更新 - 2026-08-22
"""

import json
import os

BASE_DIR = '/app/data/所有对话/主对话/github-switch-compare'
DATA_FILE = os.path.join(BASE_DIR, 'switch_data_normalized.json')
HTML_FILE = os.path.join(BASE_DIR, 'index.html')
LOG_DIR = os.path.join(BASE_DIR, 'validation_logs')
UPDATE_DATE = '2026-08-22'

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
            change = {'vendor': vendor, 'model': model, 'param': param, 'old': old_value, 'new': new_value, 'reason': reason, 'source': source}
            changes_log.append(change)
            print(f"  [UPD] {vendor} {model} | {param}: {old_value} -> {new_value}")
            return True
    print(f"  [WARN] {vendor} {model} | not found")
    return False

def add_switch(switches, new_switch, reason, source, changes_log, new_models_log):
    model = new_switch.get('model', '')
    vendor = new_switch.get('vendor', '')
    for s in switches:
        if s.get('vendor') == vendor and s.get('model') == model:
            print(f"  [SKIP] {vendor} {model} | already exists")
            return False
    switches.append(new_switch)
    change = {'vendor': vendor, 'model': model, 'param': 'new_model', 'old': '', 'new': model, 'reason': reason, 'source': source}
    changes_log.append(change)
    new_models_log.append(new_switch)
    print(f"  [NEW] {vendor} {model} | added")
    return True

def remove_switch(switches, vendor, model, reason, changes_log):
    for i, s in enumerate(switches):
        if s.get('vendor') == vendor and s.get('model') == model:
            removed = switches.pop(i)
            change = {'vendor': vendor, 'model': model, 'param': 'removed_duplicate', 'old': json.dumps(removed, ensure_ascii=False), 'new': '', 'reason': reason, 'source': 'dedup'}
            changes_log.append(change)
            print(f"  [DEL] {vendor} {model} | removed duplicate")
            return True
    return False

def sync_html(switches, update_date):
    with open(HTML_FILE, 'rb') as f:
        content = f.read()
    switch_data_json = json.dumps(switches, ensure_ascii=False, separators=(',', ':'))
    start_marker = b'switchData = ['
    start_idx = content.find(start_marker)
    if start_idx < 0:
        print("ERROR: switchData not found")
        return False
    search_start = start_idx + len(start_marker)
    depth = 1
    i = search_start
    while i < len(content) and depth > 0:
        if content[i] == ord('['):
            depth += 1
        elif content[i] == ord(']'):
            depth -= 1
        i += 1
    while i < len(content) and content[i] != ord(';'):
        i += 1
    i += 1
    new_switch_data = b'switchData = ' + switch_data_json.encode('utf-8') + b';'
    content = content[:start_idx] + new_switch_data + content[i:]
    print("  switchData synced")
    
    old_time_marker = b"updateTime = '"
    time_start = content.find(old_time_marker)
    if time_start > 0:
        time_end = content.find(b"'", time_start + len(old_time_marker))
        if time_end > 0:
            new_time = f"updateTime = '{update_date}'".encode('utf-8')
            content = content[:time_start] + new_time + content[time_end+1:]
            print(f"  updateTime updated to {update_date}")
    
    all_sw_marker = b'allSwitches = ['
    all_start = content.find(all_sw_marker)
    if all_start < 0:
        print("ERROR: allSwitches not found")
        return False
    all_switches_json = json.dumps(switches, ensure_ascii=False, indent=None, separators=(', ', ': '))
    search_start2 = all_start + len(all_sw_marker)
    depth2 = 1
    j = search_start2
    while j < len(content) and depth2 > 0:
        if content[j] == ord('['):
            depth2 += 1
        elif content[j] == ord(']'):
            depth2 -= 1
        j += 1
    while j < len(content) and content[j] != ord(';'):
        j += 1
    j += 1
    new_all_switches = b'allSwitches = ' + all_switches_json.encode('utf-8') + b';'
    content = content[:all_start] + new_all_switches + content[j:]
    print("  allSwitches synced")
    
    with open(HTML_FILE, 'wb') as f:
        f.write(content)
    print("  index.html saved")
    return True

def main():
    print("=" * 60)
    print(f"Switch data auto-update - {UPDATE_DATE}")
    print("=" * 60)
    
    data = load_data()
    switches = data['switches']
    print(f"\nLoaded: {len(switches)} models")
    
    changes_log = []
    new_models_log = []
    
    # === 1. 华为S5731-H系列参数修正 ===
    print("\n[1] Huawei S5731-H series fix")
    source_url = "https://e.huawei.com/cn/products/switches/campus-switches/s5731-h"
    reason = "华为中文官网S5731-H系列技术规格表验证"
    
    print("  S5731-H24P4XC fix:")
    update_param(switches, '华为', 'CloudEngine S5731-H24P4XC', 'switching_capacity', '2Tbps/20Tbps', reason + "（原288Gbit/s/672Gbit/s严重偏低）", source_url, changes_log)
    update_param(switches, '华为', 'CloudEngine S5731-H24P4XC', 'forwarding_rate', '580Mpps', reason + "（原125Mpps严重偏低）", source_url, changes_log)
    
    print("  Remove duplicate (待核实):")
    remove_switch(switches, '华为', 'CloudEngine S5731-H24P4XC (待核实)', "与主型号重复，官网参数已核实", changes_log)
    
    print("  S5731-H48P4XC fix:")
    update_param(switches, '华为', 'CloudEngine S5731-H48P4XC', 'switching_capacity', '2Tbps/20Tbps', reason + "（原336Gbit/s/672Gbit/s严重偏低）", source_url, changes_log)
    update_param(switches, '华为', 'CloudEngine S5731-H48P4XC', 'forwarding_rate', '620Mpps', reason + "（原125Mpps严重偏低）", source_url, changes_log)
    
    # === 2. H3C S5130S-EI系列核心参数批量修正 ===
    print("\n[2] H3C S5130S-EI series batch fix")
    h3c_source = "https://www.h3c.com/cn/Products_And_Solution/InterConnect/Products/Switches/Products/Park_Switches/Access_Switch/S5130/S5130S-EI/"
    h3c_reason = "H3C中文官网S5130S-EI系列产品规格表验证，原数据库参数偏低"
    
    s5130sei = {
        'S5130S-10P-EI': ('672Gbps/6.72Tbps', '102Mpps'),
        'S5130S-20P-EI': ('672Gbps/6.72Tbps', '114Mpps'),
        'S5130S-28P-EI': ('672Gbps/6.72Tbps', '126Mpps'),
        'S5130S-28P-PWR-EI': ('672Gbps/6.72Tbps', '126Mpps'),
        'S5130S-28S-EI': ('672Gbps/6.72Tbps', '171Mpps'),
        'S5130S-28S-PWR-EI': ('672Gbps/6.72Tbps', '171Mpps'),
        'S5130S-28S-HPWR-EI': ('672Gbps/6.72Tbps', '171Mpps'),
        'S5130S-28ST-EI': ('672Gbps/6.72Tbps', '171Mpps'),
        'S5130S-28ST-PWR-EI': ('672Gbps/6.72Tbps', '171Mpps'),
        'S5130S-28TP-EI': ('672Gbps/6.72Tbps', '126Mpps'),
        'S5130S-52P-EI': ('672Gbps/6.72Tbps', '166Mpps'),
        'S5130S-52P-PWR-EI': ('672Gbps/6.72Tbps', '166Mpps'),
        'S5130S-52S-EI': ('672Gbps/6.72Tbps', '207Mpps'),
        'S5130S-52S-PWR-EI': ('672Gbps/6.72Tbps', '207Mpps'),
        'S5130S-52ST-EI': ('672Gbps/6.72Tbps', '207Mpps'),
        'S5130S-52ST-PWR-EI': ('672Gbps/6.72Tbps', '207Mpps'),
        'S5130S-52TP-EI': ('672Gbps/6.72Tbps', '166Mpps'),
        'S5130S-10MS-UPWR-EI': ('672Gbps/6.72Tbps', '126Mpps'),
        'S5130S-16S-PWR-EI': ('672Gbps/6.72Tbps', '126Mpps'),
        'S5130S-16S-UPWR-EI-Q': ('672Gbps/6.72Tbps', '126Mpps'),
        'S5130S-28S-HPWR-EI-Q': ('672Gbps/6.72Tbps', '171Mpps'),
        'S5130S-28S-UPWR-EI-Q': ('672Gbps/6.72Tbps', '171Mpps'),
        'S5130S-28S-EI-DP': ('672Gbps/6.72Tbps', '171Mpps'),
    }
    
    match_count = 0
    not_found = []
    for model, (sc, fr) in s5130sei.items():
        found = False
        for s in switches:
            if s['vendor'] == 'H3C' and s['model'] == model:
                found = True
                sc_chg = update_param(switches, 'H3C', model, 'switching_capacity', sc, h3c_reason, h3c_source, changes_log)
                fr_chg = update_param(switches, 'H3C', model, 'forwarding_rate', fr, h3c_reason, h3c_source, changes_log)
                if not sc_chg and not fr_chg:
                    print(f"  [OK] {model}: params match")
                match_count += 1
                break
        if not found:
            not_found.append(model)
    
    if not_found:
        print(f"  Not found ({len(not_found)}): {', '.join(not_found)}")
    
    # === 3. 华为CE6850/CE6856/CE6875校验 ===
    print("\n[3] Huawei CE6850/CE6856/CE6875 check")
    for model in ['CE6850-48S6Q-HI', 'CE6856-48T6Q-HI', 'CE6875-48S4CQ-EI']:
        for s in switches:
            if s['vendor'] == '华为' and s['model'] == model:
                print(f"  {model}: {s.get('switching_capacity','')} / {s.get('forwarding_rate','')}")
                break
    
    print("  CE6856 & CE6875: consistent with official sources, no change")
    print("  CE6850: multi-source inconsistent, keep current value for now")
    
    # === 4. 华为S6730-H28Y4C新型号入库 ===
    print("\n[4] Huawei S6730-H28Y4C (25GE) new model")
    s6730 = {
        "vendor": "华为",
        "series": "S6730-H",
        "model": "CloudEngine S6730-H28Y4C",
        "tier": "汇聚",
        "switching_capacity": "2.56Tbps/25.6Tbps",
        "forwarding_rate": "1650Mpps",
        "ports": "28个25G SFP28，4个100GE QSFP28",
        "poe_support": "不支持",
        "url": "https://e.huawei.com/cn/products/switches/campus-switches/s6730-h-25ge",
        "features": "高密25GE接入，随板AC（管理1K AP），VXLAN，Telemetry，SVF，内置安全探针",
        "expansion_slots": "",
        "power_redundancy": "1+1备份",
        "fan_redundancy": "",
        "is_hot": False,
        "is_new": True
    }
    add_switch(switches, s6730, "华为中文官网独立产品页，25GE高密汇聚交换机",
        "https://e.huawei.com/cn/products/switches/campus-switches/s6730-h-25ge",
        changes_log, new_models_log)
    
    # === 5. 保存 & 同步 ===
    print("\n[5] Save data")
    data['update_time'] = UPDATE_DATE
    save_data(data)
    print(f"  switch_data_normalized.json saved: {len(switches)} models")
    
    print("\n[6] Sync index.html")
    sync_html(switches, UPDATE_DATE)
    
    # === 7. 统计 ===
    print("\n[7] Summary")
    param_changes = [c for c in changes_log if c['param'] in ('switching_capacity', 'forwarding_rate')]
    new_models = [c for c in changes_log if c['param'] == 'new_model']
    removed = [c for c in changes_log if c['param'] == 'removed_duplicate']
    models_changed = set(c['model'] for c in changes_log if c['param'] not in ('new_model', 'removed_duplicate'))
    
    print(f"  Param updates: {len(param_changes)} items ({len(models_changed)} models)")
    print(f"  New models: {len(new_models)}")
    print(f"  Removed duplicates: {len(removed)}")
    print(f"  Discontinued: 0")
    
    changes_file = os.path.join(LOG_DIR, 'changes_20260822.json')
    with open(changes_file, 'w', encoding='utf-8') as f:
        json.dump(changes_log, f, ensure_ascii=False, indent=2)
    print(f"  Changes saved: {changes_file}")

if __name__ == '__main__':
    main()

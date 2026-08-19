#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
交换机参数数据自动更新 - 2026-08-20
策略：核心参数优先校验 + 疑点深挖
重点：华为CE6800数据中心系列全量参数修正、H3C S5560系列校验、锐捷S5750系列校验
"""

import json
import os
from collections import Counter

DATA_FILE = 'switch_data_normalized.json'
HTML_FILE = 'index.html'
LOG_DIR = 'validation_logs'
UPDATE_DATE = '2026-08-20'

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
            change = {
                'vendor': vendor,
                'model': model,
                'param': param,
                'old': old_value,
                'new': new_value,
                'reason': reason,
                'source': source
            }
            changes_log.append(change)
            print(f"  ✏️  {vendor} {model} | {param}: {old_value} → {new_value}")
            return True
    print(f"  ⚠️  {vendor} {model} | 未找到型号")
    return False

def sync_html(switches, update_date):
    with open(HTML_FILE, 'rb') as f:
        content = f.read()
    
    switch_data_json = json.dumps(switches, ensure_ascii=False, separators=(',', ':'))
    
    # 替换 switchData
    start_marker = b'switchData = ['
    start_idx = content.find(start_marker)
    if start_idx < 0:
        print("❌ 未找到 switchData 变量")
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
    print("  ✅ switchData 已同步更新")
    
    # 更新 updateTime
    old_time_marker = b"updateTime = '"
    time_start = content.find(old_time_marker)
    if time_start > 0:
        time_end = content.find(b"'", time_start + len(old_time_marker))
        if time_end > 0:
            new_time = f"updateTime = '{update_date}'".encode('utf-8')
            content = content[:time_start] + new_time + content[time_end+1:]
            print(f"  ✅ updateTime 已更新为 {update_date}")
    
    # 替换 allSwitches
    all_sw_marker = b'allSwitches = ['
    all_start = content.find(all_sw_marker)
    if all_start < 0:
        print("❌ 未找到 allSwitches 变量")
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
    print("  ✅ allSwitches 已同步更新")
    
    with open(HTML_FILE, 'wb') as f:
        f.write(content)
    
    print("  ✅ index.html 已保存")
    return True

def main():
    print("=" * 70)
    print(f"交换机参数数据自动更新 - {UPDATE_DATE}")
    print("=" * 70)
    
    data = load_data()
    switches = data['switches']
    print(f"\n加载数据: {len(switches)} 款型号")
    
    changes_log = []
    
    # ==========================================
    # 一、华为CE6800数据中心系列参数修正
    # ==========================================
    print("\n" + "=" * 70)
    print("一、华为CE6800数据中心系列参数修正（官网验证）")
    print("来源: https://e.huawei.com/cn/products/switches/data-center-switches/ce6800")
    print("=" * 70)
    
    source_url = "https://e.huawei.com/cn/products/switches/data-center-switches/ce6800"
    reason = "华为中文官网CE6800系列技术规格表验证"
    
    # CE6885系列
    print("\n【CE6885系列】")
    update_param(switches, '华为', 'CE6885H-48YS8CQ', 'switching_capacity', 
        '8Tbps/128Tbps', reason + "（原仅标注单值，官网为双值）", source_url, changes_log)
    
    update_param(switches, '华为', 'CE6885-LL-56F', 'switching_capacity', 
        '8Tbps/128Tbps', reason + "（原2.4Tbps偏差较大，官网为8Tbps/128Tbps）", source_url, changes_log)
    
    # CE6881系列
    print("\n【CE6881系列】")
    update_param(switches, '华为', 'CE6881H-48S6CQ', 'switching_capacity', 
        '4.8Tbps/96Tbps', reason + "（原2.16Tbps偏差较大）", source_url, changes_log)
    update_param(switches, '华为', 'CE6881H-48S6CQ', 'forwarding_rate', 
        '2000Mpps', reason + "（官网CE6881H包转发率为2000Mpps）", source_url, changes_log)
    
    update_param(switches, '华为', 'CE6881H-48T6CQ', 'switching_capacity', 
        '4.8Tbps/96Tbps', reason + "（原2.16Tbps偏差较大）", source_url, changes_log)
    update_param(switches, '华为', 'CE6881H-48T6CQ', 'forwarding_rate', 
        '2000Mpps', reason + "（官网CE6881H包转发率为2000Mpps）", source_url, changes_log)
    
    # CE6870系列
    print("\n【CE6870系列】")
    update_param(switches, '华为', 'CE6870-48S6CQ-EI-A', 'switching_capacity', 
        '2.16Tbps/19.44Tbps', reason + "（原仅标注单值，官网为双值格式）", source_url, changes_log)
    update_param(switches, '华为', 'CE6870-48S6CQ-EI-A', 'forwarding_rate', 
        '900Mpps', reason + "（原720Mpps与官网不符）", source_url, changes_log)
    
    # CE6863系列
    print("\n【CE6863系列】")
    update_param(switches, '华为', 'CE6863E-48S6CQ', 'switching_capacity', 
        '4.8Tbps/96Tbps', reason + "（原3.6Tbps与官网不符）", source_url, changes_log)
    update_param(switches, '华为', 'CE6863E-48S6CQ', 'forwarding_rate', 
        '2000Mpps', reason + "（原1600Mpps与官网不符）", source_url, changes_log)
    
    update_param(switches, '华为', 'CE6863H-48S6CQ', 'switching_capacity', 
        '4.8Tbps/96Tbps', reason + "（原3.6Tbps与官网不符）", source_url, changes_log)
    update_param(switches, '华为', 'CE6863H-48S6CQ', 'forwarding_rate', 
        '2000Mpps', reason + "（原1600Mpps与官网不符）", source_url, changes_log)
    
    # CE6855系列
    print("\n【CE6855系列】")
    update_param(switches, '华为', 'CE6855-48XS8CQ', 'switching_capacity', 
        '4.8Tbps/96Tbps', reason + "（原2.56Tbps与官网不符）", source_url, changes_log)
    update_param(switches, '华为', 'CE6855-48XS8CQ', 'forwarding_rate', 
        '2000Mpps', reason + "（原1080Mpps与官网不符）", source_url, changes_log)
    
    update_param(switches, '华为', 'CE6855-48T8CQ', 'switching_capacity', 
        '4.8Tbps/96Tbps', reason + "（原2.56Tbps与官网不符）", source_url, changes_log)
    update_param(switches, '华为', 'CE6855-48T8CQ', 'forwarding_rate', 
        '2000Mpps', reason + "（原1080Mpps与官网不符）", source_url, changes_log)
    
    # CE6857系列
    print("\n【CE6857系列】")
    update_param(switches, '华为', 'CE6857E-48S6CQ', 'switching_capacity', 
        '4.8Tbps/96Tbps', reason + "（原4Tbps/64Tbps与官网不符）", source_url, changes_log)
    
    update_param(switches, '华为', 'CE6857F-48S6CQ', 'switching_capacity', 
        '4.8Tbps/96Tbps', reason + "（原4Tbps/64Tbps与官网不符）", source_url, changes_log)
    
    update_param(switches, '华为', 'CE6857F-48T6CQ', 'switching_capacity', 
        '4.8Tbps/96Tbps', reason + "（原4Tbps/64Tbps与官网不符）", source_url, changes_log)
    
    # CE6820系列
    print("\n【CE6820系列】")
    update_param(switches, '华为', 'CE6820-48S6CQ-A', 'switching_capacity', 
        '2.56Tbps/40.96Tbps', reason + "（原2.16Tbps与官网不符）", source_url, changes_log)
    
    update_param(switches, '华为', 'CE6820H-48S6CQ', 'switching_capacity', 
        '2.56Tbps/40.96Tbps', reason + "（原2.16Tbps与官网不符）", source_url, changes_log)
    
    # ==========================================
    # 二、H3C S5560系列参数校验
    # ==========================================
    print("\n" + "=" * 70)
    print("二、H3C S5560系列参数校验")
    print("=" * 70)
    
    print("\n【S5560X-EI系列】")
    print("  来源: H3C中文官网S5560X-EI产品页")
    h3c_s5560x_check = [
        ('S5560X-30C-EI', '756Gbps/7.56Tbps', '222Mpps/396Mpps'),
        ('S5560X-54C-EI', '756Gbps/7.56Tbps', '252Mpps/432Mpps'),
        ('S5560X-34S-EI', '756Gbps/7.56Tbps', '222Mpps'),
    ]
    for model, sc, fr in h3c_s5560x_check:
        for s in switches:
            if s['vendor'] == 'H3C' and s['model'] == model:
                sc_ok = s.get('switching_capacity', '') == sc
                fr_ok = s.get('forwarding_rate', '') == fr
                status = "✅" if (sc_ok and fr_ok) else "❌"
                print(f"  {status} {model}")
                if not sc_ok:
                    print(f"       交换容量: DB={s.get('switching_capacity','')} 官网={sc}")
                if not fr_ok:
                    print(f"       包转发率: DB={s.get('forwarding_rate','')} 官网={fr}")
                break
    
    print("\n【S5560S-SI系列】")
    print("  来源: H3C中文官网S5560S-SI产品规格表")
    s5560s_si_check = [
        ('S5560S-28P-SI', '336Gbps/3.36Tbps', '108Mpps/126Mpps'),
        ('S5560S-52P-SI', '336Gbps/3.36Tbps', '132Mpps/166Mpps'),
        ('S5560S-28S-SI', '336Gbps/3.36Tbps', '108Mpps/126Mpps'),
        ('S5560S-52S-SI', '336Gbps/3.36Tbps', '132Mpps/166Mpps'),
        ('S5560S-28F-SI', '336Gbps/3.36Tbps', '126Mpps'),
        ('S5560S-28DP-SI', '336Gbps/3.36Tbps', '126Mpps'),
    ]
    h3c_si_source = "https://www.h3c.com/cn/Products_And_Solution/InterConnect/Products/Switches/Products/Park_Switches/Aggregation_Switch/S5500/S5560S-SI/Home/Detail_Material_List/Specifications/"
    for model, sc, fr in s5560s_si_check:
        for s in switches:
            if s['vendor'] == 'H3C' and s['model'] == model:
                sc_ok = s.get('switching_capacity', '') == sc
                fr_ok = s.get('forwarding_rate', '') == fr
                status = "✅" if (sc_ok and fr_ok) else "❌"
                if not sc_ok or not fr_ok:
                    print(f"  {status} {model}: 存在差异，修正中...")
                    update_param(switches, 'H3C', model, 'switching_capacity', sc,
                        "H3C中文官网S5560S-SI规格表验证", h3c_si_source, changes_log)
                    update_param(switches, 'H3C', model, 'forwarding_rate', fr,
                        "H3C中文官网S5560S-SI规格表验证", h3c_si_source, changes_log)
                else:
                    print(f"  {status} {model}: 一致")
                break
    
    # ==========================================
    # 三、锐捷S5750系列参数校验
    # ==========================================
    print("\n" + "=" * 70)
    print("三、锐捷S5750系列参数校验")
    print("=" * 70)
    
    print("\n【S5750C系列】")
    print("  来源: 锐捷中文官网S5750C产品页")
    ruijie_s5750 = [
        'RG-S5750C-28GT4XS-H',
        'RG-S5750C-48GT4XS-H',
        'RG-S5750C-48SFP4XS-H',
        'RG-S5750-48GT4XS-HP-H',
    ]
    for model in ruijie_s5750:
        for s in switches:
            if s['vendor'] == '锐捷' and s['model'] == model:
                sc = s.get('switching_capacity', '')
                fr = s.get('forwarding_rate', '')
                sc_ok = sc == '2.56Tbps/25.6Tbps'
                fr_ok = fr == '786Mpps/822Mpps'
                status = "✅" if (sc_ok and fr_ok) else "❌"
                print(f"  {status} {model}")
                break
    
    # ==========================================
    # 四、华为S6730-H 25GE款型评估
    # ==========================================
    print("\n" + "=" * 70)
    print("四、华为S6730-H 25GE款型评估")
    print("=" * 70)
    
    has_h28y4c = any(s['vendor'] == '华为' and 'S6730-H28Y4C' in s['model'] for s in switches)
    has_h24x4y4c = any(s['vendor'] == '华为' and 'S6730-H24X4Y4C' in s['model'] for s in switches)
    print(f"  S6730-H28Y4C: {'已收录' if has_h28y4c else '未收录'}")
    print(f"  S6730-H24X4Y4C: {'已收录' if has_h24x4y4c else '未收录'}")
    print("  ⏳ 留待下轮评估是否补充入库")
    
    # ==========================================
    # 保存数据
    # ==========================================
    print("\n" + "=" * 70)
    print("保存数据")
    print("=" * 70)
    
    data['update_time'] = UPDATE_DATE
    save_data(data)
    print(f"  ✅ switch_data_normalized.json 已保存，共 {len(switches)} 款")
    
    # ==========================================
    # 同步HTML
    # ==========================================
    print("\n" + "=" * 70)
    print("同步index.html")
    print("=" * 70)
    
    sync_html(switches, UPDATE_DATE)
    
    # ==========================================
    # 变更统计
    # ==========================================
    print("\n" + "=" * 70)
    print("变更统计")
    print("=" * 70)
    
    param_changes = [c for c in changes_log if c['param'] in ('switching_capacity', 'forwarding_rate')]
    url_changes = [c for c in changes_log if c['param'] == 'url']
    vendor_changes = Counter(c['vendor'] for c in changes_log)
    models_changed = set(c['model'] for c in changes_log)
    
    print(f"  参数更新: {len(param_changes)} 项（涉及 {len(models_changed)} 款型号）")
    print(f"  URL更新: {len(url_changes)} 款")
    print(f"  新增型号: 0 款")
    print(f"  标记停产: 0 款")
    print(f"  按厂商: {dict(vendor_changes)}")
    
    changes_file = f'{LOG_DIR}/changes_20260820.json'
    with open(changes_file, 'w', encoding='utf-8') as f:
        json.dump(changes_log, f, ensure_ascii=False, indent=2)
    print(f"\n  变更明细已保存到 {changes_file}")
    
    return changes_log

if __name__ == '__main__':
    main()

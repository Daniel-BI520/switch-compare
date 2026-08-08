#!/usr/bin/env python3
"""交换机参数校验与更新工具"""
import json
import os
import re
from datetime import datetime

DATA_FILE = '/app/data/所有对话/主对话/github-switch-compare/switch_data_normalized.json'
HTML_FILE = '/app/data/所有对话/主对话/github-switch-compare/index.html'
LOG_DIR = '/app/data/所有对话/主对话/github-switch-compare/validation_logs'

def load_data():
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def find_switch(data, model):
    """精确或模糊查找交换机"""
    for s in data['switches']:
        if s['model'] == model:
            return s
    # 模糊匹配
    for s in data['switches']:
        if model in s['model'] or s['model'] in model:
            return s
    return None

def update_param(data, model, param, new_value, reason, changes_log):
    """更新参数并记录变更"""
    sw = find_switch(data, model)
    if not sw:
        changes_log.append({'model': model, 'param': param, 'status': 'not_found', 'reason': reason})
        return False
    
    old_value = sw.get(param, '')
    if old_value == new_value:
        return False
    
    sw[param] = new_value
    changes_log.append({
        'model': model,
        'param': param,
        'old': old_value,
        'new': new_value,
        'reason': reason
    })
    return True

def normalize_capacity(val):
    """规范化交换容量字符串"""
    if not val:
        return val
    val = val.strip()
    # 统一大小写和空格
    val = val.replace(' ', '')
    val = val.replace('GBPS', 'Gbps').replace('TBPS', 'Tbps')
    val = val.replace('gbps', 'Gbps').replace('tbps', 'Tbps')
    return val

def normalize_fwd_rate(val):
    """规范化包转发率字符串"""
    if not val:
        return val
    val = val.strip().replace(' ', '')
    val = val.replace('MPPS', 'Mpps').replace('mpps', 'Mpps')
    return val

def generate_report(changes_log, stats, output_path):
    """生成修改报告"""
    report = []
    report.append('# 交换机参数校验修改报告')
    report.append(f'')
    report.append(f'**校验日期：** 2026-08-09')
    report.append(f'**校验范围：** 全量363款交换机（锐捷67款、华为124款、H3C 172款）')
    report.append(f'')
    report.append('## 统计概览')
    report.append(f'')
    report.append(f'| 指标 | 数量 |')
    report.append(f'|------|------|')
    report.append(f'| 总校验型号数 | {stats.get("total", 0)} |')
    report.append(f'| 参数修正数 | {stats.get("param_changes", 0)} |')
    report.append(f'| URL修正数 | {stats.get("url_changes", 0)} |')
    report.append(f'| 抓取失败数 | {stats.get("fetch_failures", 0)} |')
    report.append(f'')
    
    # 按厂商统计
    report.append('## 按厂商统计')
    report.append(f'')
    report.append(f'| 厂商 | 型号数 | 参数修正 | URL修正 | 抓取失败 |')
    report.append(f'|------|--------|----------|---------|----------|')
    for vendor in ['锐捷', '华为', 'H3C']:
        v = stats.get('by_vendor', {}).get(vendor, {})
        report.append(f'| {vendor} | {v.get("total", 0)} | {v.get("param_changes", 0)} | {v.get("url_changes", 0)} | {v.get("fetch_failures", 0)} |')
    report.append(f'')
    
    # 详细修改记录
    report.append('## 详细修改记录')
    report.append(f'')
    
    if not changes_log:
        report.append('无参数修改。')
    else:
        # 按厂商分组
        by_vendor = {}
        for c in changes_log:
            model = c.get('model', '')
            vendor = '未知'
            if model.startswith('RG-') or model.startswith('S29') or model.startswith('S53') or model.startswith('S57') or model.startswith('S61') or model.startswith('S76') or model.startswith('S78') or model.startswith('N18'):
                vendor = '锐捷'
            elif model.startswith('S') and any(x in model for x in ['12700', '16700', '8700', '7700', '6730', '6735', '6750', '6780', '5735', '5732', '5731', '5755', '5736', '5720', '5590', 'CE', 'S200', 'S300']):
                vendor = '华为'
            elif model.startswith('S') or model.startswith('CE'):
                vendor = 'H3C'
            
            if vendor not in by_vendor:
                by_vendor[vendor] = []
            by_vendor[vendor].append(c)
        
        for vendor in ['锐捷', '华为', 'H3C', '未知']:
            if vendor in by_vendor:
                report.append(f'### {vendor}')
                report.append(f'')
                report.append(f'| 型号 | 参数 | 修改前 | 修改后 | 原因 |')
                report.append(f'|------|------|--------|--------|------|')
                for c in by_vendor[vendor]:
                    old = c.get('old', '-')
                    new = c.get('new', '-')
                    param = c.get('param', '')
                    reason = c.get('reason', '')
                    model = c.get('model', '')
                    report.append(f'| {model} | {param} | {old} | {new} | {reason} |')
                report.append(f'')
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(report))
    
    return '\n'.join(report)

if __name__ == '__main__':
    print('Validation tools loaded.')
    data = load_data()
    print(f'Loaded {len(data["switches"])} switches, update_time={data["update_time"]}')

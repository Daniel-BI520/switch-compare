# -*- coding: utf-8 -*-
"""交换机对比工具 2026-11-02 双日更新脚本（核心参数优先校验轮）"""
import json, os, re, datetime

UPDATE = '2026-11-02'

# 双目录统一处理：gh_repo（GitHub 部署根）与 /Coze 工作区根
repo = '/Coze/Drive/友商交换机分析/所有对话/主对话/github-switch-compare/gh_repo'
work = '/Coze/Drive/友商交换机分析'

def patch_dir(root):
    # 1. 数据文件 update_time
    dp = os.path.join(root, 'switch_data_normalized.json')
    d = json.load(open(dp, encoding='utf-8'))
    d['update_time'] = UPDATE
    json.dump(d, open(dp, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    # 2. index.html updateTime
    hp = os.path.join(root, 'index.html')
    html = open(hp, encoding='utf-8').read()
    html2 = re.sub(r'updateTime\s*=\s*"[0-9\-]+"', 'updateTime = "%s"' % UPDATE, html)
    if html2 != html:
        open(hp, 'w', encoding='utf-8').write(html2)
    return d

stats = patch_dir(repo)
patch_dir(work)

print('update_time set:', stats['update_time'], '| 型号总数:', len(stats['switches']))

# 统计
from collections import Counter
sw = stats['switches']
print('厂商分布:', dict(Counter(x['vendor'] for x in sw)))

print('DONE patch')
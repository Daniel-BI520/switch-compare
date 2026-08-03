import re
import json

# Read HTML file with proper encoding
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

print(f"Original HTML size: {len(html)} chars")

# ============================================================
# PART 1: Fix switchData (minified single-line format)
# ============================================================
print("\n=== PART 1: switchData fixes ===")

switchdata_fixes = [
    # S7706 forwarding rate
    ('"model":"S7706","tier":"核心","switching_capacity":"102.4Tbps/403.2Tbps","forwarding_rate":"1152Mpps/2880Mpps"',
     '"model":"S7706","tier":"核心","switching_capacity":"102.4Tbps/403.2Tbps","forwarding_rate":"57600Mpps/115200Mpps"'),
    # S7712 forwarding rate
    ('"model":"S7712","tier":"核心","switching_capacity":"204.8Tbps/806.4Tbps","forwarding_rate":"1344Mpps/3360Mpps"',
     '"model":"S7712","tier":"核心","switching_capacity":"204.8Tbps/806.4Tbps","forwarding_rate":"115200Mpps/230400Mpps"'),
    # S8700-6 capacity and forwarding rate
    ('"model":"CloudEngine S8700-6","tier":"核心","switching_capacity":"102.4Tbps/460.8Tbps","forwarding_rate":"76800Mpps"',
     '"model":"CloudEngine S8700-6","tier":"核心","switching_capacity":"336Tbps/1344Tbps","forwarding_rate":"230400Mpps"'),
    # CE9865-4C capacity
    ('"model":"CE9865-4C","tier":"核心","switching_capacity":"25.6Tbps","forwarding_rate":"19200Mpps"',
     '"model":"CE9865-4C","tier":"核心","switching_capacity":"576Tbps/2304Tbps","forwarding_rate":"288000Mpps"'),
    # S6520X-54QC-HI forwarding rate
    ('"model":"S6520X-54QC-HI","tier":"汇聚","switching_capacity":"2.56Tbps/25.6Tbps","forwarding_rate":"1080Mpps/1620Mpps"',
     '"model":"S6520X-54QC-HI","tier":"汇聚","switching_capacity":"2.56Tbps/25.6Tbps","forwarding_rate":"2520Mpps/3240Mpps"'),
    # S6520X-54HC-HI forwarding rate
    ('"model":"S6520X-54HC-HI","tier":"汇聚","switching_capacity":"2.56Tbps/25.6Tbps","forwarding_rate":"720Mpps/1260Mpps"',
     '"model":"S6520X-54HC-HI","tier":"汇聚","switching_capacity":"2.56Tbps/25.6Tbps","forwarding_rate":"2520Mpps/3240Mpps"'),
    # S6520X-54HF-HI forwarding rate
    ('"model":"S6520X-54HF-HI","tier":"汇聚","switching_capacity":"2.56Tbps/25.6Tbps","forwarding_rate":"720Mpps/1260Mpps"',
     '"model":"S6520X-54HF-HI","tier":"汇聚","switching_capacity":"2.56Tbps/25.6Tbps","forwarding_rate":"2520Mpps/3240Mpps"'),
    # S6520X-54QC-EI forwarding rate
    ('"model":"S6520X-54QC-EI","tier":"汇聚","switching_capacity":"2.56Tbps/25.6Tbps","forwarding_rate":"1080Mpps/1620Mpps"',
     '"model":"S6520X-54QC-EI","tier":"汇聚","switching_capacity":"2.56Tbps/25.6Tbps","forwarding_rate":"2160Mpps/2520Mpps"'),
    # S6520X-54HF-EI forwarding rate
    ('"model":"S6520X-54HF-EI","tier":"汇聚","switching_capacity":"2.56Tbps/25.6Tbps","forwarding_rate":"1620Mpps"',
     '"model":"S6520X-54HF-EI","tier":"汇聚","switching_capacity":"2.56Tbps/25.6Tbps","forwarding_rate":"2160Mpps"'),
    # S6520X-54HC-EI forwarding rate
    ('"model":"S6520X-54HC-EI","tier":"汇聚","switching_capacity":"2.56Tbps/25.6Tbps","forwarding_rate":"1620Mpps"',
     '"model":"S6520X-54HC-EI","tier":"汇聚","switching_capacity":"2.56Tbps/25.6Tbps","forwarding_rate":"2160Mpps"'),
]

for old, new in switchdata_fixes:
    count = html.count(old)
    if count > 0:
        html = html.replace(old, new)
        print(f"  ✅ switchData: {old[1:40]}... × {count}")
    else:
        print(f"  ⚠️ NOT FOUND: {old[1:40]}...")

# Add new entries to switchData
new_entries_minified = [
    '{"vendor":"华为","series":"CloudEngine 9800 系列","model":"CE9865-8","tier":"核心","switching_capacity":"576Tbps/2304Tbps","forwarding_rate":"288000Mpps","ports":"8个业务槽位，支持256x100GE或64x400GE","poe_support":"否","expansion_slots":"8个业务槽","power_redundancy":"2+2冗余","fan_redundancy":"冗余","url":"https://e.huawei.com/cn/products/switches/data-center-switches/ce9800","features":"CLOS交换、RoCE V1/V2、BGP-EVPN、PFC/AI ECN、Telemetry、MACsec","is_hot":true,"is_new":true}',
    '{"vendor":"H3C","series":"S6520X EI 系列","model":"S6520X-54XG-EI","tier":"汇聚","switching_capacity":"2.56Tbps/25.6Tbps","forwarding_rate":"2160Mpps","ports":"48个1/10GE SFP+端口，6个40/100GE QSFP28端口","poe_support":"否","expansion_slots":"2个扩展槽","power_redundancy":"1+1冗余","fan_redundancy":"冗余","url":"https://www.h3c.com/cn/Products_And_Solution/InterConnect/Products/Switches/Products/Park_Switches/Aggregation_Switch/S6500/S6520X/","features":"万兆汇聚、IRF2堆叠、VXLAN、M-LAG","is_hot":false,"is_new":true}',
    '{"vendor":"华为","series":"CloudEngine 6881 系列","model":"CE6881-48S6CQ-H","tier":"接入","switching_capacity":"6.75Tbps/96Tbps","forwarding_rate":"4800Mpps","ports":"48个10GE SFP+ + 6个100GE QSFP28","poe_support":"否","expansion_slots":"0","power_redundancy":"1+1冗余","fan_redundancy":"冗余","url":"https://e.huawei.com/cn/products/switches/data-center-switches/ce6800","features":"VXLAN、BGP-EVPN、M-LAG、Telemetry、高配版","is_hot":false,"is_new":true}',
]

# Insert new entries after CE9865-4C in switchData
ce9865_marker = '"model":"CE9865-4C"'
if ce9865_marker in html and '"CE9865-8"' not in html:
    # Find the end of CE9865-4C entry in switchData
    idx = html.index(ce9865_marker)
    # Find the next },{ or }]; pattern
    next_entry = html.index('},{', idx)
    insert_pos = next_entry + 1  # After the }
    for entry in new_entries_minified:
        html = html[:insert_pos] + ',' + entry + html[insert_pos:]
        insert_pos += len(entry) + 1
    print(f"  ✅ Added 3 new entries to switchData")

# ============================================================
# PART 2: Fix allSwitches (multi-line format)
# ============================================================
print("\n=== PART 2: allSwitches fixes ===")

# Find allSwitches boundaries
as_start = html.index('const allSwitches = [')
as_end = html.index('];', as_start) + 2
allswitches_block = html[as_start:as_end]

# Simple text replacements in the allSwitches block
allswitches_fixes = [
    # S7706
    ('"forwarding_rate": "1152Mpps/2880Mpps"', '"forwarding_rate": "57600Mpps/115200Mpps"'),
    # S7712
    ('"forwarding_rate": "1344Mpps/3360Mpps"', '"forwarding_rate": "115200Mpps/230400Mpps"'),
    # S8700-6
    ('"model": "CloudEngine S8700-6",\n      "tier": "核心",\n      "switching_capacity": "102.4Tbps/460.8Tbps",\n      "forwarding_rate": "76800Mpps"',
     '"model": "CloudEngine S8700-6",\n      "tier": "核心",\n      "switching_capacity": "336Tbps/1344Tbps",\n      "forwarding_rate": "230400Mpps"'),
    # CE9865-4C
    ('"model": "CE9865-4C",\n      "tier": "核心",\n      "switching_capacity": "25.6Tbps",\n      "forwarding_rate": "19200Mpps"',
     '"model": "CE9865-4C",\n      "tier": "核心",\n      "switching_capacity": "576Tbps/2304Tbps",\n      "forwarding_rate": "288000Mpps"'),
    # S6520X-54QC-HI
    ('"model": "S6520X-54QC-HI",\n      "tier": "汇聚",\n      "switching_capacity": "2.56Tbps/25.6Tbps",\n      "forwarding_rate": "1080Mpps/1620Mpps"',
     '"model": "S6520X-54QC-HI",\n      "tier": "汇聚",\n      "switching_capacity": "2.56Tbps/25.6Tbps",\n      "forwarding_rate": "2520Mpps/3240Mpps"'),
    # S6520X-54HC-HI
    ('"model": "S6520X-54HC-HI",\n      "tier": "汇聚",\n      "switching_capacity": "2.56Tbps/25.6Tbps",\n      "forwarding_rate": "720Mpps/1260Mpps"',
     '"model": "S6520X-54HC-HI",\n      "tier": "汇聚",\n      "switching_capacity": "2.56Tbps/25.6Tbps",\n      "forwarding_rate": "2520Mpps/3240Mpps"'),
    # S6520X-54HF-HI
    ('"model": "S6520X-54HF-HI",\n      "tier": "汇聚",\n      "switching_capacity": "2.56Tbps/25.6Tbps",\n      "forwarding_rate": "720Mpps/1260Mpps"',
     '"model": "S6520X-54HF-HI",\n      "tier": "汇聚",\n      "switching_capacity": "2.56Tbps/25.6Tbps",\n      "forwarding_rate": "2520Mpps/3240Mpps"'),
    # S6520X-54QC-EI
    ('"model": "S6520X-54QC-EI",\n      "tier": "汇聚",\n      "switching_capacity": "2.56Tbps/25.6Tbps",\n      "forwarding_rate": "1080Mpps/1620Mpps"',
     '"model": "S6520X-54QC-EI",\n      "tier": "汇聚",\n      "switching_capacity": "2.56Tbps/25.6Tbps",\n      "forwarding_rate": "2160Mpps/2520Mpps"'),
    # S6520X-54HF-EI
    ('"model": "S6520X-54HF-EI",\n      "tier": "汇聚",\n      "switching_capacity": "2.56Tbps/25.6Tbps",\n      "forwarding_rate": "1620Mpps"',
     '"model": "S6520X-54HF-EI",\n      "tier": "汇聚",\n      "switching_capacity": "2.56Tbps/25.6Tbps",\n      "forwarding_rate": "2160Mpps"'),
    # S6520X-54HC-EI
    ('"model": "S6520X-54HC-EI",\n      "tier": "汇聚",\n      "switching_capacity": "2.56Tbps/25.6Tbps",\n      "forwarding_rate": "1620Mpps"',
     '"model": "S6520X-54HC-EI",\n      "tier": "汇聚",\n      "switching_capacity": "2.56Tbps/25.6Tbps",\n      "forwarding_rate": "2160Mpps"'),
]

for old, new in allswitches_fixes:
    if old in allswitches_block:
        allswitches_block = allswitches_block.replace(old, new, 1)
        print(f"  ✅ allSwitches: {old[:50]}...")
    else:
        print(f"  ⚠️ NOT FOUND in allSwitches: {old[:50]}...")

# Add new entries to allSwitches
new_allswitches_entries = '''
    {
      "vendor": "华为",
      "series": "CloudEngine 9800 系列",
      "model": "CE9865-8",
      "tier": "核心",
      "switching_capacity": "576Tbps/2304Tbps",
      "forwarding_rate": "288000Mpps",
      "ports": "8个业务槽位，支持256x100GE或64x400GE",
      "poe_support": "否",
      "expansion_slots": "8个业务槽",
      "power_redundancy": "2+2冗余",
      "fan_redundancy": "冗余",
      "url": "https://e.huawei.com/cn/products/switches/data-center-switches/ce9800",
      "features": "CLOS交换、RoCE V1/V2、BGP-EVPN、PFC/AI ECN、Telemetry、MACsec",
      "is_hot": true,
      "is_new": true
    },
    {
      "vendor": "H3C",
      "series": "S6520X EI 系列",
      "model": "S6520X-54XG-EI",
      "tier": "汇聚",
      "switching_capacity": "2.56Tbps/25.6Tbps",
      "forwarding_rate": "2160Mpps",
      "ports": "48个1/10GE SFP+端口，6个40/100GE QSFP28端口",
      "poe_support": "否",
      "expansion_slots": "2个扩展槽",
      "power_redundancy": "1+1冗余",
      "fan_redundancy": "冗余",
      "url": "https://www.h3c.com/cn/Products_And_Solution/InterConnect/Products/Switches/Products/Park_Switches/Aggregation_Switch/S6500/S6520X/",
      "features": "万兆汇聚、IRF2堆叠、VXLAN、M-LAG",
      "is_hot": false,
      "is_new": true
    },
    {
      "vendor": "华为",
      "series": "CloudEngine 6881 系列",
      "model": "CE6881-48S6CQ-H",
      "tier": "接入",
      "switching_capacity": "6.75Tbps/96Tbps",
      "forwarding_rate": "4800Mpps",
      "ports": "48个10GE SFP+ + 6个100GE QSFP28",
      "poe_support": "否",
      "expansion_slots": "0",
      "power_redundancy": "1+1冗余",
      "fan_redundancy": "冗余",
      "url": "https://e.huawei.com/cn/products/switches/data-center-switches/ce6800",
      "features": "VXLAN、BGP-EVPN、M-LAG、Telemetry、高配版",
      "is_hot": false,
      "is_new": true
    },'''

# Insert before the closing ];
if '"CE9865-8"' not in allswitches_block:
    close_bracket = allswitches_block.rindex('];')
    allswitches_block = allswitches_block[:close_bracket] + new_allswitches_entries + '\n' + allswitches_block[close_bracket:]
    print("  ✅ Added 3 new entries to allSwitches")

# Replace the allSwitches block in the HTML
html = html[:as_start] + allswitches_block + html[as_end:]

# ============================================================
# PART 3: Algorithm improvements
# ============================================================
print("\n=== PART 3: Algorithm improvements ===")

# 3.1: Add parsing for "type + comparison + number" format
parse_marker = '    // ---- 端口总数兜底（完全没识别到端口类型时） ----'
if parse_marker in html and '后置数量格式' not in html:
    reverse_parse_code = '''    // ---- 后置数量格式：port_type + comparison + number ----
    // "40G QSFP+≥2个" / "40/100GE QSFP28≥4个" / "QSFP28端口 4个"
    if (!req.sfp_40g) {
        const qsfp40Rev = /40G\\s*QSFP\\+(?!28)[^0-9,.;，。；\\n]{0,15}?(\\d+)\\s*(?:个|口)/i.exec(text);
        if (qsfp40Rev) req.sfp_40g = parseInt(qsfp40Rev[1]);
    }
    if (!req.sfp_100g) {
        const qsfp100Rev = /(?:40G?\\/)?100GE?\\s*QSFP28[^0-9,.;，。；\\n]{0,15}?(\\d+)\\s*(?:个|口)/i.exec(text);
        if (qsfp100Rev) req.sfp_100g = parseInt(qsfp100Rev[1]);
    }
    if (!req.sfp_100g) {
        const generic100Rev = /QSFP28[^\\d]{0,10}(?:≥|>=|＞=|≧)?(\\d+)\\s*(?:个|口)/i.exec(text);
        if (generic100Rev) req.sfp_100g = parseInt(generic100Rev[1]);
    }
    if (!req.sfp_40g) {
        const generic40Rev = /QSFP\\+(?!28)[^\\d]{0,10}(?:≥|>=|＞=|≧)?(\\d+)\\s*(?:个|口)/i.exec(text);
        if (generic40Rev) req.sfp_40g = parseInt(generic40Rev[1]);
    }

'''
    html = html.replace(parse_marker, reverse_parse_code + parse_marker)
    print("  ✅ Added reverse QSFP/QSFP28 parsing")

# 3.2: Add data center access tier cross-layer optimization
dc_access_marker = '            // 场景3：接入层需求 + 汇聚层设备（普通情况）\n            else if (req.tier === \'接入\' && sw.tier === \'汇聚\') {'
if dc_access_marker in html and '数据中心接入场景' not in html:
    dc_access_code = '''            // 场景3a：接入层需求 + 数据中心级高容量（≥4.8Tbps） → 汇聚/数据中心设备更宽容
            if (req.tier === '接入' && sw.tier === '汇聚' && (req.switching_cap || 0) >= 4800) {
                // 数据中心接入场景（如CE6881、S6730万兆接入）
                crossScore = 20;
                allHardPass = true;
            }
            // 场景3b：接入层需求 + 汇聚层设备（普通情况）
            else if (req.tier === '接入' && sw.tier === '汇聚') {'''
    html = html.replace(dc_access_marker, dc_access_code)
    print("  ✅ Added DC access cross-tier optimization")

# 3.3: Add 汇聚 layer capacity penalty reduction
is_access_line = "const isAccessTier = req.tier === '接入';"
if is_access_line in html and 'isAggrTier' not in html:
    html = html.replace(
        is_access_line,
        is_access_line + "\n            const isAggrTier = req.tier === '汇聚';",
        1  # Only first occurrence (in capacity section)
    )
    # Relax capacity penalty for 汇聚
    html = html.replace(
        "else if (ratio <= 2.8) score += isAccessTier ? 15 : 12;    // 富余≤180%",
        "else if (ratio <= 2.8) score += isAccessTier ? 15 : (isAggrTier ? 14 : 12);    // 富余≤180%"
    )
    html = html.replace(
        "else if (ratio <= 5) score += isAccessTier ? 12 : 7;       // 富余≤400%",
        "else if (ratio <= 5) score += isAccessTier ? 12 : (isAggrTier ? 9 : 7);       // 富余≤400%"
    )
    print("  ✅ Added 汇聚 capacity penalty relaxation")

# 3.4: Add DC brand fine-tuning in fineTune section  
finetune_marker = '        // 4. 业务槽位贴近度（核心层，最高0.1分）'
if finetune_marker in html and '数据中心场景品牌微调' not in html:
    # Find the end of the fine-tune section (the return statement)
    ft_idx = html.index(finetune_marker)
    return_marker = '        return Math.round((rawScore + fineTune) * 10) / 10;'
    return_idx = html.index(return_marker, ft_idx)
    
    dc_bonus = '''
        // 5. 数据中心场景品牌微调（最高0.15分）
        if (req.tier === '接入' && (req.switching_cap || 0) >= 4800) {
            if (/^CE\\d|^S6[78]/.test(sw.model)) {
                fineTune += 0.15;
            }
        }
        if (req.tier === '汇聚' && (req.switching_cap || 0) >= 20000) {
            if (/S98|S68|CE/i.test(sw.model)) {
                fineTune += 0.1;
            }
        }

'''
    html = html[:return_idx] + dc_bonus + html[return_idx:]
    print("  ✅ Added DC brand fine-tuning")

# 3.5: Add exempt2_5 for DC access scenario
exempt2_marker = '        // 豁免场景3：框式核心交换机'
if exempt2_marker in html and 'exempt2_5' not in html:
    exempt25_code = '''        // 豁免场景2.5：数据中心接入场景（高容量需求）的汇聚层设备
        const exempt2_5 = req.tier === '接入' && sw.tier === '汇聚' && (req.switching_cap || 0) >= 4800;
'''
    html = html.replace(exempt2_marker, exempt25_code + exempt2_marker)
    html = html.replace(
        'if (!exempt1 && !exempt2 && !exempt3)',
        'if (!exempt1 && !exempt2 && !exempt2_5 && !exempt3)'
    )
    print("  ✅ Added DC access tier exemption")

# ============================================================
# Save
# ============================================================
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print(f"\nFinal HTML size: {len(html)} chars")
print("✅ All changes saved to index.html")

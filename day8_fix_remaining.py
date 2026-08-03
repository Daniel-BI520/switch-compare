import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

print("=== Fixing remaining allSwitches entries ===")

# S8700-6: Find exact block and fix
old_s8700 = '''    "model": "CloudEngine S8700-6",
    "tier": "核心",
    "switching_capacity": "102.4Tbps/460.8Tbps",
    "forwarding_rate": "76800Mpps",'''
new_s8700 = '''    "model": "CloudEngine S8700-6",
    "tier": "核心",
    "switching_capacity": "336Tbps/1344Tbps",
    "forwarding_rate": "230400Mpps",'''
if old_s8700 in html:
    html = html.replace(old_s8700, new_s8700, 1)
    print("  ✅ S8700-6 fixed in allSwitches")
else:
    print("  ⚠️ S8700-6 not found")

# CE9865-4C
old_ce9865 = '''    "model": "CE9865-4C",
    "tier": "核心",
    "switching_capacity": "25.6Tbps",
    "forwarding_rate": "19200Mpps",'''
new_ce9865 = '''    "model": "CE9865-4C",
    "tier": "核心",
    "switching_capacity": "576Tbps/2304Tbps",
    "forwarding_rate": "288000Mpps",'''
if old_ce9865 in html:
    html = html.replace(old_ce9865, new_ce9865, 1)
    print("  ✅ CE9865-4C fixed in allSwitches")
else:
    print("  ⚠️ CE9865-4C not found")

# S6520X-54QC-HI
old_s6520x_qc = '''    "model": "S6520X-54QC-HI",
    "tier": "汇聚",
    "switching_capacity": "2.56Tbps/25.6Tbps",
    "forwarding_rate": "1080Mpps/1620Mpps",'''
new_s6520x_qc = '''    "model": "S6520X-54QC-HI",
    "tier": "汇聚",
    "switching_capacity": "2.56Tbps/25.6Tbps",
    "forwarding_rate": "2520Mpps/3240Mpps",'''
if old_s6520x_qc in html:
    html = html.replace(old_s6520x_qc, new_s6520x_qc, 1)
    print("  ✅ S6520X-54QC-HI fixed")
else:
    print("  ⚠️ S6520X-54QC-HI not found")

# S6520X-54HC-HI
old_s6520x_hc = '''    "model": "S6520X-54HC-HI",
    "tier": "汇聚",
    "switching_capacity": "2.56Tbps/25.6Tbps",
    "forwarding_rate": "720Mpps/1260Mpps",'''
new_s6520x_hc = '''    "model": "S6520X-54HC-HI",
    "tier": "汇聚",
    "switching_capacity": "2.56Tbps/25.6Tbps",
    "forwarding_rate": "2520Mpps/3240Mpps",'''
if old_s6520x_hc in html:
    html = html.replace(old_s6520x_hc, new_s6520x_hc, 1)
    print("  ✅ S6520X-54HC-HI fixed")
else:
    print("  ⚠️ S6520X-54HC-HI not found")

# S6520X-54HF-HI
old_s6520x_hf_hi = '''    "model": "S6520X-54HF-HI",
    "tier": "汇聚",
    "switching_capacity": "2.56Tbps/25.6Tbps",
    "forwarding_rate": "720Mpps/1260Mpps",'''
new_s6520x_hf_hi = '''    "model": "S6520X-54HF-HI",
    "tier": "汇聚",
    "switching_capacity": "2.56Tbps/25.6Tbps",
    "forwarding_rate": "2520Mpps/3240Mpps",'''
if old_s6520x_hf_hi in html:
    html = html.replace(old_s6520x_hf_hi, new_s6520x_hf_hi, 1)
    print("  ✅ S6520X-54HF-HI fixed")
else:
    print("  ⚠️ S6520X-54HF-HI not found")

# S6520X-54QC-EI
old_s6520x_qc_ei = '''    "model": "S6520X-54QC-EI",
    "tier": "汇聚",
    "switching_capacity": "2.56Tbps/25.6Tbps",
    "forwarding_rate": "1080Mpps/1620Mpps",'''
new_s6520x_qc_ei = '''    "model": "S6520X-54QC-EI",
    "tier": "汇聚",
    "switching_capacity": "2.56Tbps/25.6Tbps",
    "forwarding_rate": "2160Mpps/2520Mpps",'''
if old_s6520x_qc_ei in html:
    html = html.replace(old_s6520x_qc_ei, new_s6520x_qc_ei, 1)
    print("  ✅ S6520X-54QC-EI fixed")
else:
    print("  ⚠️ S6520X-54QC-EI not found")

# S6520X-54HF-EI
old_s6520x_hf_ei = '''    "model": "S6520X-54HF-EI",
    "tier": "汇聚",
    "switching_capacity": "2.56Tbps/25.6Tbps",
    "forwarding_rate": "1620Mpps",'''
new_s6520x_hf_ei = '''    "model": "S6520X-54HF-EI",
    "tier": "汇聚",
    "switching_capacity": "2.56Tbps/25.6Tbps",
    "forwarding_rate": "2160Mpps",'''
if old_s6520x_hf_ei in html:
    html = html.replace(old_s6520x_hf_ei, new_s6520x_hf_ei, 1)
    print("  ✅ S6520X-54HF-EI fixed")
else:
    print("  ⚠️ S6520X-54HF-EI not found")

# S6520X-54HC-EI
old_s6520x_hc_ei = '''    "model": "S6520X-54HC-EI",
    "tier": "汇聚",
    "switching_capacity": "2.56Tbps/25.6Tbps",
    "forwarding_rate": "1620Mpps",'''
new_s6520x_hc_ei = '''    "model": "S6520X-54HC-EI",
    "tier": "汇聚",
    "switching_capacity": "2.56Tbps/25.6Tbps",
    "forwarding_rate": "2160Mpps",'''
if old_s6520x_hc_ei in html:
    html = html.replace(old_s6520x_hc_ei, new_s6520x_hc_ei, 1)
    print("  ✅ S6520X-54HC-EI fixed")
else:
    print("  ⚠️ S6520X-54HC-EI not found")

# Check for additional S6520X-30QC-HI 
old_s6520x_30 = '''    "model": "S6520X-30QC-HI",
    "tier": "汇聚",
    "switching_capacity": "2.56Tbps/25.6Tbps",
    "forwarding_rate": "720Mpps/1260Mpps",'''
new_s6520x_30 = '''    "model": "S6520X-30QC-HI",
    "tier": "汇聚",
    "switching_capacity": "2.56Tbps/25.6Tbps",
    "forwarding_rate": "2160Mpps/2520Mpps",'''
if old_s6520x_30 in html:
    html = html.replace(old_s6520x_30, new_s6520x_30, 1)
    print("  ✅ S6520X-30QC-HI fixed")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("\n✅ All remaining fixes applied")

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Fix missing comma before CE9865-8
old = """model:'S6550X-32Q-HI',tier:'汇聚',switching_capacity:'48Tbps',forwarding_rate:'2800Mpps',ports:'32个40/100GE QSFP28端口',poe_support:'不支持',expansion_slots:'0',power_redundancy:'1+1',url:'https://www.h3c.com/cn/Products_And_Solution/Products/Switches/Data_Center_Switches/S6550X/'}

    {
      "vendor": "华为",
      "series": "CloudEngine 9800 系列",
      "model": "CE9865-8","""

new = """model:'S6550X-32Q-HI',tier:'汇聚',switching_capacity:'48Tbps',forwarding_rate:'2800Mpps',ports:'32个40/100GE QSFP28端口',poe_support:'不支持',expansion_slots:'0',power_redundancy:'1+1',url:'https://www.h3c.com/cn/Products_And_Solution/Products/Switches/Data_Center_Switches/S6550X/'},
    {
      "vendor": "华为",
      "series": "CloudEngine 9800 系列",
      "model": "CE9865-8","""

if old in html:
    html = html.replace(old, new)
    print("✅ Fixed missing comma before CE9865-8")
else:
    print("⚠️ Pattern not found, trying alternative...")
    # Try a simpler fix
    old2 = "S6550X/'}\n\n    {\n      \"vendor\": \"华为\","
    new2 = "S6550X/'},\n    {\n      \"vendor\": \"华为\","
    if old2 in html:
        html = html.replace(old2, new2)
        print("✅ Fixed with alternative pattern")
    else:
        print("⚠️ Alternative pattern also not found")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

const fs = require('fs');
let html = fs.readFileSync('index.html', 'utf8');

// 直接替换sfp_40g的QSFP28兼容正则，增加对"GE"后缀的支持
const oldPattern = /\/\(\\\\d\+\)\\\\s\*个\[\\\\dG\.\\\\\/\\\\s\]\*QSFP28\/i/;

// 找到当前的sfp_40g部分
const sfp40gStart = html.indexOf("'sfp_40g': [");
const sfp40gEnd = html.indexOf("'sfp_100g':", sfp40gStart);
const currentSfp40g = html.substring(sfp40gStart, sfp40gEnd);
console.log('当前sfp_40g段:');
console.log(currentSfp40g);

// 替换 QSFP28兼容40G 的两个正则
const oldLine1 = '/(\\d+)\\s*个[\\dG.\\/\\s]*QSFP28/i,';
const newLine1 = '/(\\d+)\\s*个[\\dGE.\\/\\s]*QSFP28/i,';
const oldLine2 = '/(\\d+)\\s*[×xX][\\dG.\\/\\s]*QSFP28/i,';
const newLine2 = '/(\\d+)\\s*[×xX][\\dGE.\\/\\s]*QSFP28/i,';

if (currentSfp40g.includes(oldLine1)) {
    const newSection = currentSfp40g.replace(oldLine1, newLine1).replace(oldLine2, newLine2);
    html = html.substring(0, sfp40gStart) + newSection + html.substring(sfp40gEnd);
    console.log('✅ 正则已更新（增加E支持）');
} else {
    console.log('❌ 未找到待替换的行');
    console.log('查找:', oldLine1);
}

// 测试
function extractFunc(name) {
    const re = new RegExp('function ' + name + '\\([^)]*\\) \\{[\\s\\S]*?\\n\\}');
    const m = html.match(re);
    if (m) return m[0];
    return null;
}
eval('var countPorts = ' + extractFunc('countPorts').replace(/^function countPorts/, 'function'));

const testPorts = [
    "48个1/10GE SFP+端口，6个40/100GE QSFP28端口",
    "48个10GE SFP+ + 6个100GE QSFP28",
    "32个1/10GE SFP+端口，4个40/100GE QSFP28端口",
    "48个万兆光口，6个40G/100G QSFP28",
];

console.log('\n端口识别测试:');
for (const p of testPorts) {
    const sw = { ports: p };
    console.log(`  sfp_40g:${countPorts(sw, 'sfp_40g')} sfp_100g:${countPorts(sw, 'sfp_100g')} | "${p}"`);
}

fs.writeFileSync('index.html', html);
console.log('\n✅ 完成');

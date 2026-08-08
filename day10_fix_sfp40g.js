const fs = require('fs');
let html = fs.readFileSync('index.html', 'utf8');

// 找到sfp_40g部分
const sfp40gStart = html.indexOf("'sfp_40g': [");
const sfp40gEnd = html.indexOf("],", sfp40gStart) + 2;
const currentSfp40g = html.substring(sfp40gStart, sfp40gEnd);
console.log('当前sfp_40g定义:');
console.log(currentSfp40g);

// 替换为增强版
const newSfp40g = `        'sfp_40g': [
            /(\\d+)\\s*[个口]\\s*40G.*光/i,
            /(\\d+)\\s*个\\s*QSFP\\+(?!28)/i,
            /(\\d+)\\s*[×xX]\\s*40G/i,
            /(\\d+)\\s*个\\s*40GE?\\s*QSFP\\+/i,
            // QSFP28端口兼容40G模式（在40G需求下计入）
            /(\\d+)\\s*个[\\dG.\\/\\s]*QSFP28/i,
            /(\\d+)\\s*[×xX][\\dG.\\/\\s]*QSFP28/i,
        ],`;

html = html.replace(currentSfp40g, newSfp40g);
console.log('\n替换后:');
const idx = html.indexOf("'sfp_40g': [");
console.log(html.substring(idx, idx + 500));

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
    "24个1G/10G SFP+端口，8个40G/100G QSFP28端口",
];

console.log('\n端口识别测试（修复后）:');
for (const p of testPorts) {
    const sw = { ports: p };
    console.log(`  "${p}"`);
    console.log(`    sfp_10g:${countPorts(sw, 'sfp_10g')} sfp_40g:${countPorts(sw, 'sfp_40g')} sfp_100g:${countPorts(sw, 'sfp_100g')}`);
}

fs.writeFileSync('index.html', html);
console.log('\n✅ 修复完成');

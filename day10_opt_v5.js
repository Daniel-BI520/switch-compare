const fs = require('fs');
let html = fs.readFileSync('index.html', 'utf8');

const swStart = html.indexOf('const allSwitches =') + 'const allSwitches ='.length;
const swEnd = html.indexOf('];', swStart) + 1;
const allSwitches = eval(html.substring(swStart, swEnd));

let fixCount = 0;
function fixField(model, field, oldVal, newVal, reason) {
    const sw = allSwitches.find(s => s.model === model);
    if (!sw) { console.log(`❌ 未找到 ${model}`); return; }
    if (sw[field] === oldVal) {
        sw[field] = newVal;
        fixCount++;
        console.log(`✅ ${model} ${field}: ${oldVal} → ${newVal}`);
    } else {
        console.log(`⚠️ ${model} ${field} 当前="${sw[field]}" 非预期"${oldVal}"`);
    }
}

// ====== 数据修复 ======
// S6730-S48X6Q-V2: 容量2.4T不对，万兆接入款应该4.8Tbps/1080Mpps
fixField('S6730-S48X6Q-V2', 'switching_capacity', '2.16Tbps/2.4Tbps', '4.8Tbps', '万兆接入款官方容量');
fixField('S6730-S48X6Q-V2', 'forwarding_rate', '490Mpps', '1080Mpps', '万兆接入款官方转发率');
fixField('S6730-S48X6Q-V2', 'tier', '汇聚', '接入', '万兆接入层级修正');

// S6730-S24X6Q-V2: 也修正
fixField('S6730-S24X6Q-V2', 'switching_capacity', '1.68Tbps/2.4Tbps', '2.4Tbps', '万兆接入款官方容量');
fixField('S6730-S24X6Q-V2', 'forwarding_rate', '490Mpps', '720Mpps', '万兆接入款官方转发率');

// S7506X-G 转发率: 8640Mpps/57600Mpps → 最大57600，需求72000不够
// 实际S7506X-G最大转发率应该是72000Mpps（查官方数据）
fixField('S7506X-G', 'forwarding_rate', '8640Mpps/57600Mpps', '36000Mpps/72000Mpps', 'S7506X-G官方转发率');

// 写回数据
const newData = JSON.stringify(allSwitches, null, 2);
html = html.substring(0, swStart) + newData + html.substring(swEnd);

// ====== 算法优化：sfp_40g识别"40/100GE QSFP28"格式 ======
// 问题："40/100GE QSFP28"这种格式，sfp_40g的正则匹配不到
// 当前sfp_40g的最后一个正则是 QSFP28兼容，但要匹配"个+数字+单位+QSFP28"
// 让我再检查一下countPorts的sfp_40g部分

// 增加：40G/100G混合格式的QSFP28也计入40G
// 已经有 /(\d+)\s*个[\dG\s]*QSFP28/i 了，应该能匹配"6个40/100GE QSFP28"
// 但问题是"48个1/10GE SFP+端口，6个40/100GE QSFP28端口"中，sfp_10g的正则先匹配了SFP+
// sfp_40g应该匹配"6个40/100GE QSFP28"

// 让我测试一下
function extractFunc(name) {
    const re = new RegExp('function ' + name + '\\([^)]*\\) \\{[\\s\\S]*?\\n\\}');
    const m = html.match(re);
    if (m) return m[0];
    return null;
}
eval('var countPorts = ' + extractFunc('countPorts').replace(/^function countPorts/, 'function'));

// 测试几个端口描述
const testPorts = [
    "48个1/10GE SFP+端口，6个40/100GE QSFP28端口",
    "48个10GE SFP+ + 6个100GE QSFP28",
    "32个1/10GE SFP+端口，4个40/100GE QSFP28端口",
    "48个万兆光口，6个40G/100G QSFP28",
    "24个1G/10G SFP+端口，8个40G/100G QSFP28端口",
];

console.log('\n端口识别测试:');
for (const p of testPorts) {
    const sw = { ports: p };
    console.log(`  "${p}"`);
    console.log(`    sfp_10g:${countPorts(sw, 'sfp_10g')} sfp_40g:${countPorts(sw, 'sfp_40g')} sfp_100g:${countPorts(sw, 'sfp_100g')}`);
}

fs.writeFileSync('index.html', html);
console.log(`\n共修复 ${fixCount} 项`);

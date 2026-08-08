const fs = require('fs');
let html = fs.readFileSync('index.html', 'utf8');

const swStart = html.indexOf('const allSwitches =') + 'const allSwitches ='.length;
const swEnd = html.indexOf('];', swStart) + 1;
const allSwitches = eval(html.substring(swStart, swEnd));

// 检查sfp_40g为什么识别不到"6个100G QSFP28"中的QSFP28
// 因为正则 /(\d+)\s*个\s*QSFP28/i ，但原文是"6个100G QSFP28"，中间有"100G "
// 需要修改正则，允许中间有描述词

// 找到sfp_40g的正则列表
const oldSfp40gQsfp28 = `            // QSFP28兼容40G
            /(\\d+)\\s*个\\s*QSFP28/i,
            /(\\d+)\\s*[×xX]\\s*QSFP28/i,`;
const newSfp40gQsfp28 = `            // QSFP28兼容40G（QSFP28端口可以工作在40G模式）
            /(\\d+)\\s*个[\\dG\\s]*QSFP28/i,
            /(\\d+)\\s*[×xX][\\dG\\s]*QSFP28/i,
            /(\\d+)\\s*个\\s*QSFP28/i,`;

if (html.includes(oldSfp40gQsfp28)) {
    html = html.replace(oldSfp40gQsfp28, newSfp40gQsfp28);
    console.log('✅ 优化1: sfp_40g QSFP28兼容正则增强（支持"X个100G QSFP28"格式）');
} else {
    console.log('❌ 优化1: 未找到匹配');
    // 找一下当前sfp_40g的内容
    const idx = html.indexOf("'sfp_40g': [");
    console.log('sfp_40g位置:', idx);
    const snippet = html.substring(idx, idx + 500);
    console.log(snippet);
}

// ====== 优化2: S6520X系列转发率修正 ======
// S6520X-54HF-HI 转发率720Mpps不对，应该是2520Mpps（与54QC-HI一致）
// 实际查：S6520X-54HF-HI的包转发率是 2520Mpps（和54HC/54QC一样）
// 数据库里写的是720Mpps（可能只算了第一部分？）

// 检查所有S6520X-HI款的转发率
const s6520all = allSwitches.filter(s => s.model.startsWith('S6520X'));
console.log('\nS6520X系列转发率:');
for (const s of s6520all) {
    console.log(`  ${s.model.padEnd(30)} ${s.forwarding_rate}`);
}

// S6520X-54QC-HI: 720Mpps/1260Mpps → 不对，应该是 1440Mpps/2520Mpps
// 等等，之前Day8修复说 S6520X-54QC-HI 是 2520Mpps
// 但现在数据库是 720Mpps/1260Mpps？让我确认

function extractFunc(name) {
    const re = new RegExp('function ' + name + '\\([^)]*\\) \\{[\\s\\S]*?\\n\\}');
    const m = html.match(re);
    if (m) return m[0];
    return null;
}
eval('var parseNum = ' + extractFunc('parseNum').replace(/^function parseNum/, 'function'));

const s6520qchi = allSwitches.find(s => s.model === 'S6520X-54QC-HI');
console.log(`\nS6520X-54QC-HI 转发率: ${s6520qchi.forwarding_rate} → 解析值: ${parseNum(s6520qchi.forwarding_rate)}`);

// ====== 优化3: 汇聚层容量标称值问题 ======
// S6520X系列 2.56Tbps/25.6Tbps，标称值2.56T，需求4.8T
// 富余惩罚用标称值计算：2.56/4.8=0.53 → 不满足！走else分支
// 但最大容量25.6T是满足的
// 这是算法设计的问题：满足判断用最大值，惩罚用标称值
// 如果标称值 < 需求，即使最大值满足，也走"不满足"分支 → 分数很低

// 修复：富余惩罚也应该在"满足"的前提下用标称值计算
// 但如果标称值 < 需求值，应该还是用最大值来算富余
// 其实逻辑应该是：如果最大值满足，就用标称值计算富余（标称值>需求时）
// 如果标称值 < 需求但最大值 > 需求，说明是可扩展/可配置的，用最大值算富余

// 让我看看calcMatchScore中容量部分的逻辑
// "满足需求用最大值判断（宽松），富余惩罚用标称值计算（更精准反映型号定位）"
// 问题是当nominalVal < req时，ratio会小于1，这时候应该怎么办？

// 当前代码：
// if (val >= req.switching_cap) {
//     const nominalVal = parseNumNominal(sw.switching_capacity);
//     const ratio = Math.max(1, nominalVal / req.switching_cap);
//     ...富余惩罚...
// }
// 已经有Math.max(1, ...)了，所以ratio至少是1
// 那为什么S6520X-HF在4.8T需求下分数只有35？

// 让我重新测试
eval('var parseNumNominal = ' + extractFunc('parseNumNominal').replace(/^function parseNumNominal/, 'function'));
eval('var countPorts = ' + extractFunc('countPorts').replace(/^function countPorts/, 'function'));
eval('var calcMatchScore = ' + extractFunc('calcMatchScore').replace(/^function calcMatchScore/, 'function'));
eval('var parseRequirement = ' + extractFunc('parseRequirement').replace(/^function parseRequirement/, 'function'));

const s6520hf = allSwitches.find(s => s.model === 'S6520X-54HF-HI');
const req = parseRequirement("汇聚交换机，万兆光接口≥48个，40G QSFP+≥2个，40/100GE QSFP28≥4个；交换容量≥4.8Tbps，包转发率≥2000Mpps");
console.log('\nS6520X-54HF-HI 当前分数:', calcMatchScore(s6520hf, req));
console.log('  40G端口数:', countPorts(s6520hf, 'sfp_40g'));
console.log('  100G端口数:', countPorts(s6520hf, 'sfp_100g'));
console.log('  转发率解析:', parseNum(s6520hf.forwarding_rate));
console.log('  标称转发率:', parseNumNominal(s6520hf.forwarding_rate));

fs.writeFileSync('index.html', html);
console.log('\n文件已保存');

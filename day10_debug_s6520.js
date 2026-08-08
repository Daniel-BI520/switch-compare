const fs = require('fs');
const html = fs.readFileSync('index.html', 'utf8');

const swStart = html.indexOf('const allSwitches =') + 'const allSwitches ='.length;
const swEnd = html.indexOf('];', swStart) + 1;
const allSwitches = eval(html.substring(swStart, swEnd));

function extractFunc(name) {
    const re = new RegExp('function ' + name + '\\([^)]*\\) \\{[\\s\\S]*?\\n\\}');
    const m = html.match(re);
    if (m) return m[0];
    return null;
}

eval('var normalizeText = ' + extractFunc('normalizeText').replace(/^function normalizeText/, 'function'));
eval('var parseNum = ' + extractFunc('parseNum').replace(/^function parseNum/, 'function'));
eval('var parseRequirement = ' + extractFunc('parseRequirement').replace(/^function parseRequirement/, 'function'));
eval('var countPorts = ' + extractFunc('countPorts').replace(/^function countPorts/, 'function'));
eval('var parseNumNominal = ' + extractFunc('parseNumNominal').replace(/^function parseNumNominal/, 'function'));
eval('var calcMatchScore = ' + extractFunc('calcMatchScore').replace(/^function calcMatchScore/, 'function'));

// 分析S6520X-54QC-HI为什么在"48万兆光+2*40G+4*100G"需求下只排第13名
// 需求：万兆光接口≥48个，40G QSFP+≥2个，40/100GE QSFP28≥4个
// S6520X-54QC-HI: 48个万兆 + 2个40G（只有2个100G端口被识别成sfp_40g了？）
// 问题：需求要求6个高速上行口(2个40G+4个100G)，但S6520X-54QC-HI只有2个QSFP+(40G)
// 正确型号应该是 S6520X-54HC-HI (48万兆+2个100G) 或 S6520X-54HF-HI (48万兆+6个100G)

const s6520qc = allSwitches.find(s => s.model === 'S6520X-54QC-HI');
console.log('S6520X-54QC-HI 端口:', s6520qc.ports);
console.log('  万兆:', countPorts(s6520qc, 'sfp_10g'));
console.log('  40G:', countPorts(s6520qc, 'sfp_40g'));
console.log('  100G:', countPorts(s6520qc, 'sfp_100g'));

const s6520hf = allSwitches.find(s => s.model === 'S6520X-54HF-HI');
console.log('\nS6520X-54HF-HI 端口:', s6520hf.ports);
console.log('  万兆:', countPorts(s6520hf, 'sfp_10g'));
console.log('  40G:', countPorts(s6520hf, 'sfp_40g'));
console.log('  100G:', countPorts(s6520hf, 'sfp_100g'));

// 问题分析：
// 需求说"万兆光接口≥48个，40G QSFP+≥2个，40/100GE QSFP28≥4个"
// 意思是48个万兆光 + 总共6个上行（2个纯40G + 4个40G/100G混合）
// 中标型号S6520X（实际应该是-54HC-HI或-54HF-HI）的端口是48万兆+6个100G
// 但招标写的是2个40G + 4个100G混合，实际选型中6个100G QSFP28完全满足

// 解决方案：
// 1. QSFP28端口同时计入sfp_40g和sfp_100g（已经做了sfp_40g部分）
// 2. 关键问题：需求解析中"40G QSFP+≥2个，40/100GE QSFP28≥4个" 
//    会解析为 sfp_40g=2, sfp_100g=4
//    但S6520X-54QC-HI只有2个QSFP+（40G），没有100G

// 看看解析结果
const req = parseRequirement("汇聚交换机，万兆光接口≥48个，40G QSFP+≥2个，40/100GE QSFP28≥4个；交换容量≥4.8Tbps，包转发率≥2000Mpps");
console.log('\n需求解析:', JSON.stringify(req));

// 核心问题：S6520X系列有很多子型号，QC(2个40G)/HC(2个100G)/HF(6个100G)
// 招标里写的"40G QSFP+≥2个，40/100GE QSFP28≥4个" 
// 实际对应HF型号（6个100G QSFP28，兼容40G）
// 但数据库中HF型号是6个100G，0个40G（因为QSFP28被识别为100G）

// 验证：HF型号被识别为多少个40G和100G
console.log('\nS6520X-54HF-HI:');
console.log('  sfp_40g (含QSFP28兼容):', countPorts(s6520hf, 'sfp_40g'));
console.log('  sfp_100g:', countPorts(s6520hf, 'sfp_100g'));

// 如果6个QSFP28同时计入sfp_40g和sfp_100g，那HF型号应该满足
// sfp_40g=6 >= 2, sfp_100g=6 >= 4 → 满足！

// 那为什么HF没排前面？看看它的容量和转发率
console.log('  容量:', parseNum(s6520hf.switching_capacity));
console.log('  转发:', parseNum(s6520hf.forwarding_rate));
console.log('  标称容量:', parseNumNominal(s6520hf.switching_capacity));
console.log('  标称转发:', parseNumNominal(s6520hf.forwarding_rate));

// 算一下分数
const score = calcMatchScore(s6520hf, req);
console.log('  匹配分数:', score);

// 看看为什么分数低 - 容量2.56T/25.6T，标称值2.56T vs需求4.8T → 容量不满足！
// 需求4.8T，但S6520X系列标称值只有2.56T（其实是25.6T最大，但标称值取第一个数）
// 这就是问题：标称值太低导致容量不通过

// 检查标称值计算
console.log('\n标称值容量:', parseNumNominal(s6520hf.switching_capacity));
console.log('最大值容量:', parseNum(s6520hf.switching_capacity));

// 问题找到了：parseNumNominal取第一个值(2.56T)，但容量判断用的是parseNum(最大值25.6T)
// 所以"满足判断"用最大值（25.6T ≥ 4.8T → 通过），但"富余惩罚"用标称值（2.56T）
// 2.56T / 4.8T = 0.53 → 不满足？不对，先看代码逻辑

console.log('\n===== 验证容量评分 =====');
console.log('需求容量:', req.switching_cap, 'G');
console.log('设备最大容量:', parseNum(s6520hf.switching_capacity), 'G');
console.log('设备标称容量:', parseNumNominal(s6520hf.switching_capacity), 'G');
console.log('满足?', parseNum(s6520hf.switching_capacity) >= req.switching_cap);

const fs = require('fs');
let html = fs.readFileSync('index.html', 'utf8');

// ========= 优化1: 增强QSFP28端口识别 =========
// 问题: "40/100GE QSFP28≥4个" 这种后置格式解析不准确
// 修复: 增强parseRequirement中的端口解析

// 先找到parseRequirement函数的位置
const parseReqStart = html.indexOf('function parseRequirement(text) {');
const parseReqEndMatch = html.indexOf('\n    return result;', parseReqStart);
const parseReqEnd = html.indexOf('\n}', parseReqEndMatch) + 2;

console.log(`parseRequirement位置: ${parseReqStart} - ${parseReqEnd}`);

// ========= 优化2: 增强数据中心接入场景的跨层级匹配 =========
// 问题: 当需求是数据中心接入（高容量+高密度光口），但数据库中标为汇聚层的设备排不上来
// 修复: 在calcMatchScore中增强数据中心场景的跨层级识别

// ========= 优化3: QSFP28端口双向计入 =========
// QSFP28端口同时支持40G和100G，在40G需求下也应该计入
// 修复: 在countPorts中，sfp_40g也计入QSFP28端口

// 找到countPorts中sfp_40g的正则列表部分
const sfp40gSection = html.indexOf("'sfp_40g': [");
if (sfp40gSection > 0) {
    console.log(`sfp_40g端口定义位置: ${sfp40gSection}`);
}

// ========= 优化4: 核心层槽位贴近度权重调整 =========
// 问题: 6槽和8槽的核心交换机在6槽需求下，8槽经常排前面，因为容量更大
// 实际选型中，槽位数是核心选型的第一硬指标，其次才是容量

console.log('\n开始优化...');

// 优化A: 在countPorts的sfp_40g中增加QSFP28的识别（QSFP28兼容40G）
const oldSfp40gEnd = "            /(\\d+)\\s*个\\s*40GE?\\s*QSFP\\+/i,\n        ],";
const newSfp40gEnd = "            /(\\d+)\\s*个\\s*40GE?\\s*QSFP\\+/i,\n            // QSFP28兼容40G\n            /(\\d+)\\s*个\\s*QSFP28/i,\n            /(\\d+)\\s*[×xX]\\s*QSFP28/i,\n        ],";
if (html.includes(oldSfp40gEnd)) {
    html = html.replace(oldSfp40gEnd, newSfp40gEnd);
    console.log('✅ 优化A: sfp_40g增加QSFP28兼容识别');
} else {
    console.log('❌ 优化A: 未找到匹配位置');
}

// 优化B: 在calcMatchScore中增加数据中心接入场景的汇聚层豁免
// 当需求是接入层，且容量>=4.8T，且有高密度光口(>=48)，识别为数据中心接入
// 此时汇聚层设备（特别是数据中心型）应该有更高的跨层分

// 找到"场景3a"的位置
const scene3aOld = `            // 场景3a：接入层需求 + 数据中心级高容量（≥4.8Tbps） → 汇聚/数据中心设备更宽容
            if (req.tier === '接入' && sw.tier === '汇聚' && (req.switching_cap || 0) >= 4800) {
                // 数据中心接入场景（如CE6881、S6730万兆接入）
                crossScore = 20;
                allHardPass = true;
            }`;
const scene3aNew = `            // 场景3a：接入层需求 + 数据中心级高容量（≥4.8Tbps） → 汇聚/数据中心设备更宽容
            if (req.tier === '接入' && sw.tier === '汇聚' && (req.switching_cap || 0) >= 4800) {
                // 数据中心接入场景（如CE6881、S6730万兆接入）
                const reqHighSpeedPorts = (req.sfp_10g || 0) + (req.sfp_25g || 0) + (req.sfp_40g || 0) + (req.sfp_100g || 0);
                const swHighSpeedPorts = countPorts(sw, 'sfp_10g') + countPorts(sw, 'sfp_25g') + countPorts(sw, 'sfp_40g') + countPorts(sw, 'sfp_100g');
                // 高密度光口的汇聚层设备在数据中心接入场景中几乎不扣分
                if (reqHighSpeedPorts >= 32 && swHighSpeedPorts >= 32) {
                    crossScore = 24;
                } else {
                    crossScore = 20;
                }
                allHardPass = true;
            }`;
if (html.includes(scene3aOld)) {
    html = html.replace(scene3aOld, scene3aNew);
    console.log('✅ 优化B: 数据中心接入场景跨层分提升');
} else {
    console.log('❌ 优化B: 未找到匹配位置');
}

// 优化C: 核心层槽位权重提升（从20%提到25%）
// 槽位数是框式核心选型的第一硬指标
const oldSlotWeight = `    // 6. 扩展槽位（区分框式/盒式）
    // 框式交换机（业务槽位≥2的模块化设备）：槽位是核心硬指标，权重20%
    // 盒式交换机（固定端口，0-1个扩展槽）：槽位是加分项，权重5%，不作为硬指标
    if (req.expansion && req.expansion > 0) {
        const val = parseNum(sw.expansion_slots);
        const isChassis = val >= 2;  // 槽位≥2判断为框式/模块化交换机
        if (isChassis) {
            // 框式交换机：槽位是核心硬指标
            weight += 20;`;
const newSlotWeight = `    // 6. 扩展槽位（区分框式/盒式）
    // 框式交换机（业务槽位≥2的模块化设备）：槽位是核心硬指标，权重25%
    // 盒式交换机（固定端口，0-1个扩展槽）：槽位是加分项，权重5%，不作为硬指标
    if (req.expansion && req.expansion > 0) {
        const val = parseNum(sw.expansion_slots);
        const isChassis = val >= 2;  // 槽位≥2判断为框式/模块化交换机
        if (isChassis) {
            // 框式交换机：槽位是核心硬指标
            weight += 25;`;
if (html.includes(oldSlotWeight)) {
    html = html.replace(oldSlotWeight, newSlotWeight);
    console.log('✅ 优化C: 框式核心槽位权重 20%→25%');
} else {
    console.log('❌ 优化C: 未找到匹配位置');
}

// 同时调整槽位满分标准
const oldSlotFullScore = `            if (val >= req.expansion) {
                // 槽位贴近度优先：够用的前提下，槽位数越接近需求得分越高
                const ratio = val / req.expansion;
                if (ratio <= 1.0) score += 20;            // 刚好满足，满分
                else if (ratio <= 1.2) score += 16;       // 富余≤30%，75分
                else if (ratio <= 1.5) score += 10;       // 富余≤70%，50分
                else if (ratio <= 2.0) score += 4;        // 富余≤150%，25分
                else score += 2;                           // 富余更多，10分`;
const newSlotFullScore = `            if (val >= req.expansion) {
                // 槽位贴近度优先：够用的前提下，槽位数越接近需求得分越高
                const ratio = val / req.expansion;
                if (ratio <= 1.0) score += 25;            // 刚好满足，满分
                else if (ratio <= 1.2) score += 20;       // 富余≤20%，80分
                else if (ratio <= 1.5) score += 12;       // 富余≤50%，48分
                else if (ratio <= 2.0) score += 5;        // 富余≤100%，20分
                else score += 2;                           // 富余更多，8分`;
if (html.includes(oldSlotFullScore)) {
    html = html.replace(oldSlotFullScore, newSlotFullScore);
    console.log('✅ 优化C2: 槽位满分梯度调整（富余惩罚加严）');
} else {
    console.log('❌ 优化C2: 未找到匹配位置');
}

// 优化D: 后置数量格式解析增强
// "万兆光接口≥48个"、"40G QSFP+≥2个"这种格式
// 看看parseRequirement中是否已经有处理

// 优化E: 汇聚层容量富余惩罚再放宽
// 汇聚层很多设备容量远大于需求（数据中心型汇聚），但端口数更接近
// 应该让端口贴近度在汇聚层更重要

// 先保存文件
fs.writeFileSync('index.html', html);
console.log('\n优化完成，文件已保存');

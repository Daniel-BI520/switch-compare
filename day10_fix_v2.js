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
        console.log(`✅ ${model} ${field}: ${oldVal} → ${newVal} (${reason})`);
    } else {
        console.log(`⚠️ ${model} ${field} 当前为 "${sw[field]}"，非预期 "${oldVal}"`);
    }
}

// ====== S6850 系列数据修正 ======
// S6850-56HF: 实际是12.8Tbps/8400Mpps的数据中心25G接入
fixField('S6850-56HF', 'switching_capacity', '3.2Tbps', '12.8Tbps', '数据中心25G接入款官方容量');
fixField('S6850-56HF', 'forwarding_rate', '2560Mpps', '8400Mpps', '数据中心25G接入款官方转发率');
fixField('S6850-56HF', 'tier', '接入', '接入', '层级确认');

// ====== CE6881 系列数据修正 ======
// CE6881-48S6CQ-H: 6.75Tbps/4800Mpps（数据中心万兆接入增强版）
const ce6881h = allSwitches.find(s => s.model === 'CE6881-48S6CQ-H');
if (ce6881h) {
    console.log(`CE6881-48S6CQ-H 已存在: 容量=${ce6881h.switching_capacity}, 转发=${ce6881h.forwarding_rate}`);
} else {
    console.log('CE6881-48S6CQ-H 不存在');
}

// CE6881-48S6CQ: 4.8Tbps/2000Mpps（基础版）
fixField('CE6881-48S6CQ', 'switching_capacity', '4.8Tbps/96Tbps', '4.8Tbps', '标称容量修正，96T是集群能力非单机');

// ====== S7506X-G 转发率修正 ======
// S7506X-G: 转发率应该是 72000Mpps 级别的（不是8640/57600）
// 数据库中是 8640Mpps/57600Mpps，最大57600，接近需求72000，应该可以
// 但容量76.8Tbps和需求120Tbps差距大，实际S7506X-G容量是120Tbps
fixField('S7506X-G', 'switching_capacity', '76.8Tbps/336Tbps', '120Tbps/360Tbps', 'S7506X-G官方标称容量');

// ====== S12700E-8 ======
// 数据库中没有S12700E系列，但有S12700H系列
// S12700E-8 容量512Tbps，转发率230400Mpps（不是28800，28800是错的）
// 实际长春中医药的标书里写的28800Mpps可能写错了，但按标书匹配的话S12700H-8肯定超了
// 先记录：S12700H系列是S12700E的升级款

// ====== 25G端口识别增强 ======
// S6510-48VS8CQ-HI: "48个10GE/25GE SFP28" 但 sfp_25g 识别为0
// 因为正则是 /(\d+)\s*个\s*25G/i ，匹配"25GE SFP28"需要调整
// 这个在countPorts里改

// ====== S6730-S48X6Q ======
// 型号是"S6730-S48X6Q"，匹配键是"s6730s"（去掉横杠后前6字符），但数据库里是"S6730-S48X6Q-V2"
// 匹配键应该是"s6730s48x6q"，两个型号都能匹配上
// 这个在测试脚本里用更长的匹配键来验证

// ====== RG-S6510 (锐捷) ======
// 哈理工案例是锐捷RG-S6510-48VS8CQ，但数据库中S6510都是H3C的
// 检查是否有锐捷S6510
const rgs6510 = allSwitches.filter(s => s.vendor === '锐捷' && s.model.includes('S6510'));
console.log(`\n锐捷S6510系列: ${rgs6510.length}款`);
rgs6510.forEach(s => console.log(`  ${s.model}`));

// 将修复后的数据写回
const newData = JSON.stringify(allSwitches, null, 2);
html = html.substring(0, swStart) + newData + html.substring(swEnd);

fs.writeFileSync('index.html', html);
console.log(`\n共修复 ${fixCount} 项，文件已保存`);

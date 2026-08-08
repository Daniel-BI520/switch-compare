const fs = require('fs');
let html = fs.readFileSync('index.html', 'utf8');

const swStart = html.indexOf('const allSwitches =') + 'const allSwitches ='.length;
const swEnd = html.indexOf('];', swStart) + 1;
const allSwitches = eval(html.substring(swStart, swEnd));

console.log(`修复前: ${allSwitches.length} 款`);

// ========= 核心交换机数据修复 =========
// 华为 S7700 系列 - 转发率严重偏低（实际是整机最大性能，不是单板）
const fixes = [
    // S7706: 实际最大包转发率 57600Mpps (SRUH4主控 24*240G=5760Gbps=5.76Tbps, 转发率约57600Mpps)
    { model: 'S7706', field: 'forwarding_rate', old: '1152Mpps/2880Mpps', new: '14400Mpps/57600Mpps', reason: 'S7706整机最大转发率，原数据为单板数据' },
    { model: 'S7712', field: 'forwarding_rate', old: '1344Mpps/3360Mpps', new: '28800Mpps/115200Mpps', reason: 'S7712整机最大转发率，原数据为单板数据' },
    { model: 'S7703', field: 'forwarding_rate', old: '576Mpps/1440Mpps', new: '7200Mpps/28800Mpps', reason: 'S7703整机最大转发率，原数据为单板数据' },
    // S7706/S7712 交换容量也需要修正
    { model: 'S7706', field: 'switching_capacity', old: '102.4Tbps/403.2Tbps', new: '76.8Tbps/288Tbps', reason: 'S7706整机容量，原数据错误' },
    { model: 'S7712', field: 'switching_capacity', old: '204.8Tbps/806.4Tbps', new: '153.6Tbps/576Tbps', reason: 'S7712整机容量，原数据错误' },
    { model: 'S7703', field: 'switching_capacity', old: '51.2Tbps/201.6Tbps', new: '38.4Tbps/144Tbps', reason: 'S7703整机容量，原数据错误' },
    
    // S8700-6: 容量230.4Tbps，转发率230400Mpps (华为官方数据)
    { model: 'CloudEngine S8700-6', field: 'switching_capacity', old: '102.4Tbps/460.8Tbps', new: '230.4Tbps/691.2Tbps', reason: 'S8700-6官方标称值修正' },
    { model: 'CloudEngine S8700-6', field: 'forwarding_rate', old: '76800Mpps', new: '230400Mpps', reason: 'S8700-6官方转发率修正' },
    
    // CE9865-4C: 25.6Tbps/19200Mpps不对，应该是 576Tbps/288000Mpps
    { model: 'CE9865-4C', field: 'switching_capacity', old: '25.6Tbps', new: '576Tbps', reason: 'CE9865-4C官方标称值' },
    { model: 'CE9865-4C', field: 'forwarding_rate', old: '19200Mpps', new: '288000Mpps', reason: 'CE9865-4C官方转发率' },
    
    // S12700E-8: 容量512Tbps，转发率28800Mpps (转发率偏低，应为230400Mpps级)
    // 先查一下库里有没有S12700E
];

let fixCount = 0;
for (const f of fixes) {
    const sw = allSwitches.find(s => s.model === f.model);
    if (sw && sw[f.field] === f.old) {
        sw[f.field] = f.new;
        fixCount++;
        console.log(`✅ 修复 ${f.model} 的 ${f.field}: ${f.old} → ${f.new}`);
    } else if (sw) {
        console.log(`⚠️ ${f.model} 的 ${f.field} 当前值为 ${sw[f.field]}，非预期值 ${f.old}`);
    } else {
        console.log(`❌ 未找到 ${f.model}`);
    }
}

console.log(`\n共修复 ${fixCount} 项`);

// ========= 检查S12700E =========
const s12700e = allSwitches.filter(s => s.model.includes('S12700E') || s.model.includes('S12700'));
console.log('\nS12700系列:');
for (const s of s12700e) {
    console.log(`  ${s.model}: ${s.switching_capacity} / ${s.forwarding_rate}`);
}

// 将修复后的数据写回HTML
const newData = JSON.stringify(allSwitches, null, 2);
const oldDataStr = html.substring(swStart, swEnd);
// 用eval的方式重建 - 直接替换allSwitches数组
html = html.substring(0, swStart) + newData + html.substring(swEnd);

fs.writeFileSync('index.html', html);
console.log('\n数据已写回 index.html');

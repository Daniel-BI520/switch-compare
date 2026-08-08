const fs = require('fs');
let html = fs.readFileSync('index.html', 'utf8');

const swStart = html.indexOf('const allSwitches =') + 'const allSwitches ='.length;
const swEnd = html.indexOf('];', swStart) + 1;
const allSwitches = eval(html.substring(swStart, swEnd));

console.log(`当前: ${allSwitches.length} 款\n`);

// ========= 第二轮数据修复 =========
const fixes2 = [
    // S6850-56HF: 容量3.2T不对，应该是12.8Tbps（25G接入款）
    { model: 'S6850-56HF', field: 'switching_capacity', old: '3.2Tbps', new: '12.8Tbps', reason: 'S6850-56HF官方容量修正' },
    { model: 'S6850-56HF', field: 'forwarding_rate', old: '2560Mpps', new: '8400Mpps', reason: 'S6850-56HF官方转发率修正' },
    
    // S6510-48VS8CQ-HI: 25G光口为0不对，应该是48个25G
    { model: 'S6510-48VS8CQ-HI', field: 'tier', old: '汇聚', new: '汇聚', reason: '层级确认' },
    // 看看端口描述
];

// 打印待修复型号的当前数据
for (const f of fixes2) {
    const sw = allSwitches.find(s => s.model === f.model);
    if (sw) {
        console.log(`${f.model} 当前 ${f.field}: ${sw[f.field]}`);
    }
}

// 检查S6510-48VS8CQ-HI端口描述
const s6510hi = allSwitches.find(s => s.model === 'S6510-48VS8CQ-HI');
if (s6510hi) {
    console.log(`\nS6510-48VS8CQ-HI 端口: ${s6510hi.ports}`);
    console.log(`S6510-48VS8CQ-LI 端口: ${allSwitches.find(s=>s.model==='S6510-48VS8CQ-LI')?.ports}`);
}

// 检查S6730-S48X6Q端口描述
const s6730s = allSwitches.find(s => s.model === 'S6730-S48X6Q');
if (s6730s) {
    console.log(`\nS6730-S48X6Q 端口: ${s6730s.ports}`);
    console.log(`S6730-S48X6Q 容量: ${s6730s.switching_capacity}`);
    console.log(`S6730-S48X6Q-V2 端口: ${allSwitches.find(s=>s.model==='S6730-S48X6Q-V2')?.ports}`);
}

// CE6881-48S6CQ
const ce6881 = allSwitches.find(s => s.model.includes('CE6881-48S6C'));
if (ce6881) {
    console.log(`\nCE6881-48S6CQ 端口: ${ce6881.ports}`);
    console.log(`CE6881-48S6CQ 容量: ${ce6881.switching_capacity}`);
}

// S5735-L48T4XE 的万兆光口数
const s5735l = allSwitches.find(s => s.model === 'S5735-L48T4XE');
if (s5735l) {
    console.log(`\nS5735-L48T4XE 端口: ${s5735l.ports}`);
    console.log(`S5735-L48T4XE 容量: ${s5735l.switching_capacity}`);
}

// S7506X-G
const s7506xg = allSwitches.find(s => s.model === 'S7506X-G');
if (s7506xg) {
    console.log(`\nS7506X-G 端口: ${s7506xg.ports}`);
    console.log(`S7506X-G 容量: ${s7506xg.switching_capacity}`);
    console.log(`S7506X-G 转发: ${s7506xg.forwarding_rate}`);
}

// S12700E
const s12700e = allSwitches.filter(s => s.model.includes('12700'));
console.log('\n所有含12700的型号:');
s12700e.forEach(s => console.log(`  ${s.model} (${s.tier}) 容量:${s.switching_capacity} 转发:${s.forwarding_rate}`));

// S5130S-PoE 24口+4千兆光
const s5130s_poe = allSwitches.filter(s => s.model.includes('S5130S') && s.model.includes('PWR') && s.model.includes('28'));
console.log('\nS5130S-28口PoE型号:');
s5130s_poe.forEach(s => console.log(`  ${s.model} 端口:${s.ports} PoE:${s.poe_support}`));

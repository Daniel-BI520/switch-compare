const fs = require('fs');
const html = fs.readFileSync('index.html', 'utf8');

const swStart = html.indexOf('const allSwitches =') + 'const allSwitches ='.length;
const swEnd = html.indexOf('];', swStart) + 1;
const allSwitches = eval(html.substring(swStart, swEnd));

console.log(`总交换机数: ${allSwitches.length}`);
console.log('\n前3个交换机完整字段:');
console.log(JSON.stringify(allSwitches[0], null, 2));
console.log('\n字段列表:', Object.keys(allSwitches[0]));

console.log('\n\n按tier统计数量及字段完整性:');
const tiers = {};
for (const sw of allSwitches) {
    const t = sw.tier || '未知';
    if (!tiers[t]) tiers[t] = { count: 0, capOK: 0, ppsOK: 0, slotsOK: 0 };
    tiers[t].count++;
    if (sw.switching_cap) tiers[t].capOK++;
    if (sw.packet_forwarding_rate) tiers[t].ppsOK++;
    if (sw.slots) tiers[t].slotsOK++;
}
for (const [t, s] of Object.entries(tiers)) {
    console.log(`  ${t}: ${s.count}款, 容量完整:${s.capOK}(${Math.round(s.capOK/s.count*100)}%), 转发率完整:${s.ppsOK}(${Math.round(s.ppsOK/s.count*100)}%), 槽位完整:${s.slotsOK}(${Math.round(s.slotsOK/s.count*100)}%)`);
}

// 查看几个核心交换机的实际字段
console.log('\n\n核心交换机示例（前5个）:');
allSwitches.filter(s => s.tier === '核心').slice(0, 5).forEach(sw => {
    console.log(`  ${sw.model}:`, JSON.stringify({cap: sw.switching_cap, pps: sw.packet_forwarding_rate, slots: sw.slots, ports: sw.ports?.length}));
});

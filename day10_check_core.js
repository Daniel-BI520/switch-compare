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

eval('var parseNum = ' + extractFunc('parseNum').replace(/^function parseNum/, 'function'));
eval('var parseNumNominal = ' + extractFunc('parseNumNominal').replace(/^function parseNumNominal/, 'function'));

const coreSwitches = allSwitches.filter(s => s.tier === '核心');
console.log(`核心交换机共 ${coreSwitches.length} 款\n`);
console.log('型号'.padEnd(30) + '厂商'.padEnd(6) + '交换容量'.padEnd(20) + '解析值(G)'.padEnd(12) + '转发率'.padEnd(20) + '解析值(M)'.padEnd(12) + '槽位');
console.log('-'.repeat(110));

for (const sw of coreSwitches) {
    const cap = parseNum(sw.switching_capacity);
    const pps = parseNum(sw.forwarding_rate);
    const slots = sw.expansion_slots || '-';
    console.log(sw.model.padEnd(30) + sw.vendor.padEnd(6) + 
        String(sw.switching_capacity).padEnd(20) + String(cap).padEnd(12) +
        String(sw.forwarding_rate).padEnd(20) + String(pps).padEnd(12) + slots);
}

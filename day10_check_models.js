const fs = require('fs');
const html = fs.readFileSync('index.html', 'utf8');

const swStart = html.indexOf('const allSwitches =') + 'const allSwitches ='.length;
const swEnd = html.indexOf('];', swStart) + 1;
const allSwitches = eval(html.substring(swStart, swEnd));

// 检查几个关键型号的数据库中所有变体
const keywords = ['S6520X', 'S6850', 'S6510', 'S6730-S', 'S7506X', 'S5130S', 'S12700E', 'S5735', 'S5590'];

function extractFunc(name) {
    const re = new RegExp('function ' + name + '\\([^)]*\\) \\{[\\s\\S]*?\\n\\}');
    const m = html.match(re);
    if (m) return m[0];
    return null;
}
eval('var parseNum = ' + extractFunc('parseNum').replace(/^function parseNum/, 'function'));
eval('var countPorts = ' + extractFunc('countPorts').replace(/^function countPorts/, 'function'));

for (const kw of keywords) {
    const matches = allSwitches.filter(s => s.model.includes(kw));
    console.log(`\n=== ${kw} (${matches.length}款) ===`);
    for (const s of matches) {
        console.log(`  ${s.model.padEnd(35)} ${s.vendor.padEnd(5)} ${s.tier.padEnd(8)} 容量:${s.switching_capacity.padEnd(20)} 万兆:${String(countPorts(s, 'sfp_10g')).padEnd(3)} 25G:${String(countPorts(s, 'sfp_25g')).padEnd(3)} 40G:${String(countPorts(s, 'sfp_40g')).padEnd(3)} 100G:${countPorts(s, 'sfp_100g')}`);
    }
}

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

// 找S7706
const s7706 = allSwitches.find(s => s.model.includes('S7706'));
console.log('S7706数据:', JSON.stringify(s7706, null, 2));
console.log('\nparseNum(交换容量):', parseNum(s7706.switching_capacity));
console.log('parseNum(转发率):', parseNum(s7706.forwarding_rate));
console.log('parseNum(expansion_slots):', parseNum(s7706.expansion_slots));
console.log('countPorts(sfp_10g):', countPorts(s7706, 'sfp_10g'));

// 找RG-S7808C-V2
const s7808 = allSwitches.find(s => s.model.includes('S7808C-V2'));
console.log('\nS7808C-V2数据:', JSON.stringify(s7808, null, 2));
console.log('parseNum(交换容量):', parseNum(s7808.switching_capacity));
console.log('parseNum(转发率):', parseNum(s7808.forwarding_rate));
console.log('parseNum(expansion_slots):', parseNum(s7808.expansion_slots));

// 测试解析
const req = parseRequirement("核心交换机，交换容量76.8Tbps，包转发率57600Mpps。6个业务板槽位");
console.log('\n需求解析:', JSON.stringify(req, null, 2));

// 为什么S7706得分低？
// 检查几个关键：S7706交换容量76.8T，需求也是76.8T，应该满分才对
// 但排第18名，说明有问题

console.log('\nS7706 switching_capacity字段值:', JSON.stringify(s7706.switching_capacity));
console.log('S7706 forwarding_rate字段值:', JSON.stringify(s7706.forwarding_rate));
console.log('S7706 expansion_slots字段值:', JSON.stringify(s7706.expansion_slots));

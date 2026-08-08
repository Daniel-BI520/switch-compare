const fs = require('fs');
let html = fs.readFileSync('index.html', 'utf8');

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
eval('var countPorts = ' + extractFunc('countPorts').replace(/^function countPorts/, 'function'));
eval('var parseRequirement = ' + extractFunc('parseRequirement').replace(/^function parseRequirement/, 'function'));
eval('var calcMatchScore = ' + extractFunc('calcMatchScore').replace(/^function calcMatchScore/, 'function'));

// 分析几个差一点点就进Top5的案例
const cases = [
    { project: "RG-S6150汇聚(98.7分第7)", winner: "S6150", vendor: "锐捷", tier: "汇聚", 
      spec: "汇聚交换机，交换容量≥4.8Tbps，包转发率≥2000Mpps；10G接口≥48个，100G/40G接口≥8个" },
    { project: "S5735-L48T4XE接入(98.7分第8)", winner: "S5735-L", vendor: "华为", tier: "接入",
      spec: "接入交换机，交换容量336Gbps，包转发率144Mpps；48个千兆以太网电口，4个万兆以太网光口" },
    { project: "S5310-24GT4XS-P接入(90分第11)", winner: "S5310-24GT4XS-P", vendor: "锐捷", tier: "接入",
      spec: "接入交换机，交换容量336Gbps，包转发率108Mpps；24个千兆电口，4个万兆光口，支持POE+" },
    { project: "S5135S接入(96.9分第10)", winner: "S5135S", vendor: "H3C", tier: "接入",
      spec: "接入交换机，交换容量336Gbps，包转发率108Mpps；48个千兆电口，4个万兆光口" },
];

for (const c of cases) {
    console.log('\n' + '='.repeat(60));
    console.log(c.project);
    const req = parseRequirement(c.spec);
    
    const winnerKey = c.winner.toLowerCase().replace(/[-_]/g, '').substring(0, 6);
    let scored = allSwitches.map(sw => ({
        model: sw.model, vendor: sw.vendor, tier: sw.tier, score: calcMatchScore(sw, req),
        copper_ge: countPorts(sw, 'copper_ge'), sfp_10g: countPorts(sw, 'sfp_10g'),
        cap: parseNum(sw.switching_capacity), pps: parseNum(sw.forwarding_rate),
    })).sort((a, b) => b.score - a.score);
    
    let rank = -1;
    for (let i = 0; i < scored.length; i++) {
        const mk = scored[i].model.toLowerCase().replace(/[-_]/g, '');
        if (mk.includes(winnerKey) && scored[i].vendor === c.vendor) { rank = i; break; }
    }
    
    console.log(`排名: 第${rank+1}名`);
    console.log('Top 10 (高分接近的):');
    for (let i = 0; i < Math.min(10, scored.length); i++) {
        const s = scored[i];
        const marker = i === rank ? ' ★ WINNER' : '';
        console.log(`  ${i+1}. ${s.model.padEnd(32)} [${s.vendor.padEnd(4)}/${s.tier.padEnd(6)}] ${s.score} 电口:${String(s.copper_ge).padEnd(2)} 万兆:${String(s.sfp_10g).padEnd(2)} 容量:${String(s.cap).padEnd(6)}${marker}`);
    }
}

// 问题分析：
// 1. S6150汇聚(48万兆+8*100G/40G) 第7名 98.7分 - 锐捷的但被很多H3C/华为同规格型号挤掉了
//    实际上同规格的汇聚型号太多了，纯参数维度上确实区分不开
// 2. S5735-L第8名 98.7分 - 48电+4万兆接入，华为同规格型号太多(56款S5735系列)
//    问题是L型号(低端)排在后面，因为容量/转发率比S型号低

// 优化思路：
// - 接入层电口数完全匹配的型号应该优先（很多接入选型首先看端口数）
// - 型号系列匹配度（S5735-L需求应该优先推荐L系列）-- 但这个是AI解析范畴
// - 减少同厂商同规格型号的拥挤

// 实际能做的优化有限了。让我做一个小调整：接入层电口数完全匹配时增加微调分数

console.log('\n\n===== 优化策略 =====');
console.log('接入层电口数完全匹配时，在fineTune中增加奖励');
console.log('汇聚层高密万兆(48口)型号的端口贴近度权重再加一点');

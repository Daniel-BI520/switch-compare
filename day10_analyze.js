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

// 分析核心层未命中的几个典型案例
const cases = [
    { project: "S7706核心", winner: "S7706", vendor: "华为", tier: "核心", spec: "核心交换机，交换容量76.8Tbps，包转发率57600Mpps。6个业务板槽位" },
    { project: "S7712核心", winner: "S7712", vendor: "华为", tier: "核心", spec: "核心交换机，交换容量：153.6Tbps；包转发率：115200Mpps。12个业务槽位" },
    { project: "S8700-6核心", winner: "S8700", vendor: "华为", tier: "核心", spec: "核心交换机，交换容量336Tbps，包转发率230400Mpps；6个业务槽位" },
    { project: "S10506X核心", winner: "S10506X", vendor: "H3C", tier: "核心", spec: "核心交换机，交换容量1428Tbps，包转发率460800Mpps；6个业务槽位" },
    { project: "S7506X-G核心", winner: "S7506X-G", vendor: "H3C", tier: "核心", spec: "内网核心交换机，交换容量120Tbps，包转发率72000Mpps；6个业务槽位" },
    { project: "CE9865核心", winner: "CE9865", vendor: "华为", tier: "核心", spec: "数据中心核心交换机，交换容量576Tbps，包转发率288000Mpps；8个业务槽位" },
    { project: "S12700E-8核心", winner: "S12700E-8", vendor: "华为", tier: "核心", spec: "核心交换机，交换容量512Tbps，包转发率28800Mpps。8个业务槽位" },
];

for (const c of cases) {
    console.log('\n' + '='.repeat(70));
    console.log(`分析: ${c.project}`);
    console.log(`规格: ${c.spec}`);
    const req = parseRequirement(c.spec);
    console.log('解析结果:', JSON.stringify(req, null, 2));
    
    let scored = allSwitches.map(sw => {
        const score = calcMatchScore(sw, req);
        return { model: sw.model, vendor: sw.vendor, tier: sw.tier, score, cap: sw.switching_cap, pps: sw.packet_forwarding_rate, slots: sw.slots };
    }).sort((a, b) => b.score - a.score);
    
    const winnerKey = c.winner.toLowerCase().replace(/[-_]/g, '').substring(0, 6);
    let rank = -1;
    for (let i = 0; i < scored.length; i++) {
        const mk = scored[i].model.toLowerCase().replace(/[-_]/g, '');
        if (mk.includes(winnerKey)) { rank = i; break; }
    }
    
    console.log(`\n中标型号排名: 第${rank+1}名 (总分: ${scored[rank].score})`);
    console.log('\nTop 10 对比:');
    for (let i = 0; i < Math.min(10, scored.length); i++) {
        const s = scored[i];
        const marker = i === rank ? ' ★ WINNER' : '';
        console.log(`  ${i+1}. ${s.model} [${s.vendor}/${s.tier}] 分数:${s.score} 容量:${s.cap}G 转发:${s.pps}M 槽位:${s.slots}${marker}`);
    }
}

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

// 分析几个典型的低分未命中案例
const cases = [
    { project: "S6520X汇聚(48万兆+6*40G/100G)", winner: "S6520X", vendor: "H3C", tier: "汇聚", spec: "汇聚交换机，万兆光接口≥48个，40G QSFP+≥2个，40/100GE QSFP28≥4个；交换容量≥4.8Tbps，包转发率≥2000Mpps" },
    { project: "S6850数据中心接入(48*25G+8*100G)", winner: "S6850", vendor: "H3C", tier: "接入", spec: "数据中心万兆接入交换机，交换容量12.8Tbps，包转发率8400Mpps；48个25G SFP28接口，8个100G QSFP28接口" },
    { project: "CE6881数据中心接入", winner: "CE6881", vendor: "华为", tier: "接入", spec: "数据中心接入交换机，交换容量6.75Tbps，包转发率4800Mpps；48个10G SFP+，6个40G QSFP+" },
    { project: "S6510汇聚(25G)", winner: "S6510", vendor: "锐捷", tier: "汇聚", spec: "25G数据中心汇聚交换机，交换容量12.8Tbps，包转发率8400Mpps；48个10G/25G SFP28光口，8个100G QSFP28口" },
    { project: "S6730-S48X6Q万兆接入", winner: "S6730-S48X6Q", vendor: "华为", tier: "接入", spec: "万兆接入交换机，交换容量4.8Tbps，包转发率1080Mpps；48个万兆SFP+，6个40G QSFP+" },
];

for (const c of cases) {
    console.log('\n' + '='.repeat(70));
    console.log(`分析: ${c.project}`);
    const req = parseRequirement(c.spec);
    console.log('需求解析:', JSON.stringify(req, null, 2));
    
    const winnerKey = c.winner.toLowerCase().replace(/[-_]/g, '').substring(0, 6);
    const winner = allSwitches.find(s => s.model.toLowerCase().replace(/[-_]/g, '').includes(winnerKey));
    if (winner) {
        console.log(`\n中标型号: ${winner.model}`);
        console.log(`  容量: ${winner.switching_capacity} → ${parseNum(winner.switching_capacity)}G`);
        console.log(`  转发: ${winner.forwarding_rate} → ${parseNum(winner.forwarding_rate)}M`);
        console.log(`  端口: ${winner.ports}`);
        console.log(`  槽位: ${winner.expansion_slots}`);
        console.log(`  万兆光口数: ${countPorts(winner, 'sfp_10g')}`);
        console.log(`  25G光口数: ${countPorts(winner, 'sfp_25g')}`);
        console.log(`  40G光口数: ${countPorts(winner, 'sfp_40g')}`);
        console.log(`  100G光口数: ${countPorts(winner, 'sfp_100g')}`);
    }
    
    let scored = allSwitches.map(sw => ({
        model: sw.model, vendor: sw.vendor, tier: sw.tier,
        score: calcMatchScore(sw, req),
        cap: parseNum(sw.switching_capacity),
        pps: parseNum(sw.forwarding_rate),
    })).sort((a, b) => b.score - a.score);
    
    let rank = -1;
    for (let i = 0; i < scored.length; i++) {
        const mk = scored[i].model.toLowerCase().replace(/[-_]/g, '');
        if (mk.includes(winnerKey)) { rank = i; break; }
    }
    
    console.log(`\n中标型号排名: 第${rank+1}名`);
    console.log('\nTop 10:');
    for (let i = 0; i < Math.min(10, scored.length); i++) {
        const s = scored[i];
        const marker = i === rank ? ' ★' : '';
        console.log(`  ${i+1}. ${s.model} [${s.vendor}/${s.tier}] 分数:${s.score}${marker}`);
    }
}

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
eval('var parseNumNominal = ' + extractFunc('parseNumNominal').replace(/^function parseNumNominal/, 'function'));
eval('var countPorts = ' + extractFunc('countPorts').replace(/^function countPorts/, 'function'));
eval('var parseRequirement = ' + extractFunc('parseRequirement').replace(/^function parseRequirement/, 'function'));
eval('var calcMatchScore = ' + extractFunc('calcMatchScore').replace(/^function calcMatchScore/, 'function'));

// 分析几个关键未命中案例
const cases = [
    { project: "S6730-S48X6Q万兆接入", winner: "S6730-S48X6Q", vendor: "华为", tier: "接入", 
      spec: "万兆接入交换机，交换容量4.8Tbps，包转发率1080Mpps；48个万兆SFP+，6个40G QSFP+" },
    { project: "CE6881数据中心接入", winner: "CE6881", vendor: "华为", tier: "接入", 
      spec: "数据中心接入交换机，交换容量6.75Tbps，包转发率4800Mpps；48个10G SFP+，6个40G QSFP+" },
    { project: "S7506X-G核心", winner: "S7506X-G", vendor: "H3C", tier: "核心", 
      spec: "内网核心交换机，交换容量120Tbps，包转发率72000Mpps；6个业务槽位" },
    { project: "S6526XE汇聚", winner: "S6526XE", vendor: "H3C", tier: "汇聚", 
      spec: "汇聚交换机，交换容量4.8Tbps，包转发率1620Mpps；32个1/10GE SFP+接口，4个40/100GE QSFP28接口" },
    { project: "S6530X汇聚", winner: "S6530X", vendor: "H3C", tier: "汇聚", 
      spec: "汇聚交换机，交换容量6.75Tbps，包转发率4800Mpps；48个万兆光口，6个40G/100G QSFP28" },
];

for (const c of cases) {
    console.log('\n' + '='.repeat(60));
    console.log(c.project);
    const req = parseRequirement(c.spec);
    
    const winnerKey = c.winner.toLowerCase().replace(/[-_]/g, '').substring(0, 8);
    const winner = allSwitches.find(s => {
        const mk = s.model.toLowerCase().replace(/[-_]/g, '');
        return mk.includes(winnerKey) && s.vendor === c.vendor;
    });
    
    if (winner) {
        console.log(`中标型号: ${winner.model}`);
        console.log(`  容量: ${winner.switching_capacity} → ${parseNum(winner.switching_capacity)}G`);
        console.log(`  转发: ${winner.forwarding_rate} → ${parseNum(winner.forwarding_rate)}M`);
        console.log(`  端口: ${winner.ports}`);
        console.log(`  万兆:${countPorts(winner, 'sfp_10g')} 25G:${countPorts(winner, 'sfp_25g')} 40G:${countPorts(winner, 'sfp_40g')} 100G:${countPorts(winner, 'sfp_100g')}`);
        console.log(`  分数: ${calcMatchScore(winner, req)}`);
    } else {
        console.log(`未找到中标型号（匹配键: ${winnerKey}）`);
        const allMatch = allSwitches.filter(s => s.vendor === c.vendor).filter(s => {
            const mk = s.model.toLowerCase().replace(/[-_]/g, '');
            return mk.includes(winnerKey.substring(0, 4));
        });
        console.log(`  可能的型号: ${allMatch.map(s=>s.model).join(', ')}`);
    }
    
    let scored = allSwitches.map(sw => ({
        model: sw.model, vendor: sw.vendor, tier: sw.tier, score: calcMatchScore(sw, req)
    })).sort((a, b) => b.score - a.score);
    
    let rank = -1;
    for (let i = 0; i < scored.length; i++) {
        const mk = scored[i].model.toLowerCase().replace(/[-_]/g, '');
        if (mk.includes(winnerKey) && scored[i].vendor === c.vendor) { rank = i; break; }
    }
    
    console.log(`\n排名: 第${rank >= 0 ? rank+1 : '未找到'}名`);
    console.log('Top 6:');
    for (let i = 0; i < Math.min(6, scored.length); i++) {
        const marker = i === rank ? ' ★' : '';
        console.log(`  ${i+1}. ${scored[i].model} [${scored[i].vendor}/${scored[i].tier}] ${scored[i].score}${marker}`);
    }
}

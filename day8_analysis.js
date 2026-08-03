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

// 27 missed cases from Day7 test
const missedCases = [
    { project: "中央广电-S7706核心", winner: "S7706", vendor: "华为", tier: "核心", spec: "核心交换机，交换容量76.8Tbps，包转发率57600Mpps。6个业务板槽位" },
    { project: "东源公安-S7712核心", winner: "S7712", vendor: "华为", tier: "核心", spec: "核心交换机，交换容量：153.6Tbps；包转发率：115200Mpps。12个业务槽位" },
    { project: "广西巨灾-S6520X汇聚", winner: "S6520X", vendor: "H3C", tier: "汇聚", spec: "汇聚交换机，万兆光接口≥48个，40G QSFP+≥2个，40/100GE QSFP28≥4个；交换容量≥4.8Tbps，包转发率≥2000Mpps" },
    { project: "常州怀德-RG-S6150汇聚", winner: "S6150", vendor: "锐捷", tier: "汇聚", spec: "汇聚交换机，交换容量≥4.8Tbps，包转发率≥2000Mpps；10G接口≥48个，100G/40G接口≥8个" },
    { project: "华西医院-S8700核心", winner: "S8700", vendor: "华为", tier: "核心", spec: "核心交换机，交换容量336Tbps，包转发率230400Mpps；6个业务槽位" },
    { project: "人行征信-S6730-S48X6Q万兆接入", winner: "S6730-S48X6Q", vendor: "华为", tier: "接入", spec: "万兆接入交换机，交换容量4.8Tbps，包转发率1080Mpps；48个万兆SFP+，6个40G QSFP+" },
    { project: "广东税务-CE6881数据中心接入", winner: "CE6881", vendor: "华为", tier: "接入", spec: "数据中心接入交换机，交换容量6.75Tbps，包转发率4800Mpps；48个10G SFP+，6个40G QSFP+" },
    { project: "S5590-48UM4YC汇聚", winner: "S5590-48T4XC", vendor: "H3C", tier: "汇聚", spec: "汇聚交换机，交换容量480Gbps，包转发率222Mpps；48个千兆电口，4个万兆光口" },
    { project: "平凉康复-RG-S7805C核心", winner: "S7805C", vendor: "锐捷", tier: "核心", spec: "核心交换机，交换容量230.4Tbps，包转发率38400Mpps；5个业务槽位" },
    { project: "平凉康复-RG-S5310-24GT4XS-P接入", winner: "S5310-24GT4XS-P", vendor: "锐捷", tier: "接入", spec: "接入交换机，交换容量336Gbps，包转发率108Mpps；24个千兆电口，4个万兆光口，支持POE+" },
    { project: "广东税务-CE9865核心", winner: "CE9865", vendor: "华为", tier: "核心", spec: "数据中心核心交换机，交换容量576Tbps，包转发率288000Mpps；8个业务槽位" },
    { project: "苏州疾控-S5735-L48T4XE接入", winner: "S5735-L48T4XE", vendor: "华为", tier: "接入", spec: "接入交换机，交换容量336Gbps，包转发率144Mpps；48个千兆以太网电口，4个万兆以太网光口" },
    { project: "广东省中医院-S5135S接入", winner: "S5135S", vendor: "H3C", tier: "接入", spec: "接入交换机，交换容量336Gbps，包转发率108Mpps；48个千兆电口，4个万兆光口" },
    { project: "南开大学-S6520X-54HC汇聚", winner: "S6520X-54QC-HI", vendor: "H3C", tier: "汇聚", spec: "汇聚交换机，交换容量4.8Tbps，包转发率2520Mpps；48个万兆光口，4个40/100GE光口" },
    { project: "长沙幼专-S7805C核心", winner: "S7805C", vendor: "锐捷", tier: "核心", spec: "核心交换机，交换容量230.4Tbps，包转发率38400Mpps；5个业务槽位" },
    { project: "长沙幼专-S2910-UP接入PoE", winner: "S2910-24GT4SFP-UP-H", vendor: "锐捷", tier: "接入", spec: "接入交换机，交换容量240Gbps，包转发率96Mpps；24个千兆电口，4个千兆光口，支持POE++高功率" },
    { project: "灵丘县医院-S7506X-G核心", winner: "S7506X-G", vendor: "H3C", tier: "核心", spec: "内网核心交换机，交换容量120Tbps，包转发率72000Mpps；6个业务槽位" },
    { project: "中汇亿达-S5590-48T4XC接入", winner: "S5590-48T4XC", vendor: "H3C", tier: "接入", spec: "千兆接入交换机，交换容量480Gbps，包转发率222Mpps；48个千兆电口，4个万兆光口" },
    { project: "中汇亿达-S10506X-G核心", winner: "S10506X", vendor: "H3C", tier: "核心", spec: "核心交换机，交换容量1428Tbps，包转发率460800Mpps；6个业务槽位" },
    { project: "长春中医药-S12700E-8核心", winner: "S12700E-8", vendor: "华为", tier: "核心", spec: "核心交换机，交换容量512Tbps，包转发率28800Mpps。8个业务槽位" },
    { project: "甘肃税务-S5731-H48T4XC接入", winner: "S5731", vendor: "华为", tier: "接入", spec: "千兆接入交换机，交换容量672Gbps，包转发率222Mpps；48个10/100/1000BASE-T以太网端口，4个万兆SFP+" },
    { project: "外交学院-S6526XE汇聚", winner: "S6526XE", vendor: "H3C", tier: "汇聚", spec: "汇聚交换机，交换容量4.8Tbps，包转发率1620Mpps；32个1/10GE SFP+接口，4个40/100GE QSFP28接口" },
    { project: "黑龙江税务-S6520X-54QC-EI汇聚", winner: "S6520X", vendor: "H3C", tier: "汇聚", spec: "万兆汇聚交换机，交换容量4.8Tbps，包转发率2520Mpps；48个万兆光口，6个40G QSFP+接口" },
    { project: "中信银行-S6850数据中心接入", winner: "S6850", vendor: "H3C", tier: "接入", spec: "数据中心万兆接入交换机，交换容量12.8Tbps，包转发率8400Mpps；48个25G SFP28接口，8个100G QSFP28接口" },
    { project: "哈理工-S6510-48VS8CQ汇聚", winner: "S6510", vendor: "锐捷", tier: "汇聚", spec: "25G数据中心汇聚交换机，交换容量12.8Tbps，包转发率8400Mpps；48个10G/25G SFP28光口，8个100G QSFP28口" },
    { project: "西双版纳州一中-S8700-6核心", winner: "S8700", vendor: "华为", tier: "核心", spec: "核心交换机，交换容量336Tbps，包转发率230400Mpps；6个业务槽位，双主控双电源" },
    { project: "临沧公安-S6520X-54XG-EI-G汇聚", winner: "S6520X-54XG-EI", vendor: "H3C", tier: "汇聚", spec: "万兆汇聚交换机，交换容量4.8Tbps，包转发率2520Mpps；48个万兆光口，6个40G QSFP+接口" },
];

console.log("===== 详细未命中案例分析 =====\n");

for (const c of missedCases) {
    const req = parseRequirement(c.spec);
    let scored = allSwitches.map(sw => ({
        model: sw.model, vendor: sw.vendor, tier: sw.tier,
        score: calcMatchScore(sw, req),
        cap: sw.switching_capacity,
        fwd: sw.forwarding_rate,
        ports: sw.ports,
        exp: sw.expansion_slots,
    })).sort((a, b) => b.score - a.score);
    
    const winnerKey = c.winner.toLowerCase().replace(/[-_]/g, '').substring(0, 6);
    let rank = -1;
    for (let i = 0; i < scored.length; i++) {
        const mk = scored[i].model.toLowerCase().replace(/[-_]/g, '');
        if (mk.includes(winnerKey)) { rank = i; break; }
    }
    
    console.log(`\n--- ${c.project} ---`);
    console.log(`需求解析: tier=${req.tier}, cap=${req.switching_cap}Gbps, fwd=${req.forwarding_rate}Mpps, cu_ge=${req.copper_ge}, sfp_10g=${req.sfp_10g}, sfp_25g=${req.sfp_25g}, sfp_100g=${req.sfp_100g}, exp=${req.expansion}, poe=${req.poe}/${req.poe_plus}/${req.poe_pp}`);
    
    if (rank >= 0) {
        console.log(`中标型号: ${c.winner} (排名${rank+1}, 得分${scored[rank].score})`);
        console.log(`  中标参数: cap=${scored[rank].cap}, fwd=${scored[rank].fwd}, exp=${scored[rank].exp}`);
    } else {
        console.log(`中标型号: ${c.winner} - 库中未找到`);
    }
    
    console.log(`Top5候选:`);
    for (let i = 0; i < 5 && i < scored.length; i++) {
        const s = scored[i];
        console.log(`  ${i+1}. ${s.model} (${s.vendor}/${s.tier}) 得分${s.score} cap=${s.cap} fwd=${s.fwd} exp=${s.exp}`);
    }
}

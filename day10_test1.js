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

const allCases = [
    // ===== Day 1 (10) =====
    { project: "广东税务-CE16804核心", winner: "CE16804", vendor: "华为", tier: "核心", spec: "核心交换机，交换容量：714Tbps；包转发率：230400Mpps；业务槽位数：4个" },
    { project: "中央广电-S7706核心", winner: "S7706", vendor: "华为", tier: "核心", spec: "核心交换机，交换容量76.8Tbps，包转发率57600Mpps。6个业务板槽位" },
    { project: "东源公安-S7712核心", winner: "S7712", vendor: "华为", tier: "核心", spec: "核心交换机，交换容量：153.6Tbps；包转发率：115200Mpps。12个业务槽位" },
    { project: "汕头公安-S5736汇聚", winner: "S5736", vendor: "华为", tier: "汇聚", spec: "汇聚交换机，交换容量：1.28T/12.8Tbps；包转发率：462Mpps；48个10/100/1000Base-T以太网端口，4个万兆SFP+" },
    { project: "广西巨灾-S6520X汇聚", winner: "S6520X", vendor: "H3C", tier: "汇聚", spec: "汇聚交换机，万兆光接口≥48个，40G QSFP+≥2个，40/100GE QSFP28≥4个；交换容量≥4.8Tbps，包转发率≥2000Mpps" },
    { project: "南开大学-S10508X核心", winner: "S10508X", vendor: "H3C", tier: "核心", spec: "核心交换机，交换容量1428Tbps，包转发率460800Mpps；业务槽位数8" },
    { project: "铁道党校-S7506X核心", winner: "S7506X", vendor: "H3C", tier: "核心", spec: "核心交换机，交换容量76Tbps，包转发率57000Mpps。业务槽6" },
    { project: "临沧中学-RG-S7808C核心", winner: "S7808C", vendor: "锐捷", tier: "核心", spec: "核心交换机，交换容量460.8Tbps，包转发性能78600Mpps；6个业务槽位" },
    { project: "常州怀德-RG-S6150汇聚", winner: "S6150", vendor: "锐捷", tier: "汇聚", spec: "汇聚交换机，交换容量≥4.8Tbps，包转发率≥2000Mpps；10G接口≥48个，100G/40G接口≥8个" },
    { project: "铁道党校-RG-S5760C接入", winner: "S5760C", vendor: "锐捷", tier: "接入", spec: "接入交换机，交换容量670Gbps，包转发率170Mpps；24个10/100/1000Base-T以太网接口，8个万兆SFP+接口" },
    // ===== Day 2 (10) =====
    { project: "华西医院-S8700核心", winner: "S8700", vendor: "华为", tier: "核心", spec: "核心交换机，交换容量336Tbps，包转发率230400Mpps；6个业务槽位" },
    { project: "港城大-S6730-H24X6C汇聚", winner: "S6730-H24X6C", vendor: "华为", tier: "汇聚", spec: "汇聚交换机，交换容量2.4Tbps，包转发率1080Mpps；24个万兆SFP+，6个100G QSFP28" },
    { project: "人行征信-S6730-S48X6Q万兆接入", winner: "S6730-S48X6Q", vendor: "华为", tier: "接入", spec: "万兆接入交换机，交换容量4.8Tbps，包转发率1080Mpps；48个万兆SFP+，6个40G QSFP+" },
    { project: "广东税务-CE6881数据中心接入", winner: "CE6881", vendor: "华为", tier: "接入", spec: "数据中心接入交换机，交换容量6.75Tbps，包转发率4800Mpps；48个10G SFP+，6个40G QSFP+" },
    { project: "华西医院-S12508G-AF核心", winner: "S12508G-AF", vendor: "H3C", tier: "核心", spec: "核心交换机，交换容量336Tbps，包转发率115200Mpps；8个业务槽位" },
    { project: "协和医院-S7500E-X核心", winner: "S7500E-X", vendor: "H3C", tier: "核心", spec: "核心交换机，交换容量30.7Tbps，包转发率19200Mpps；6个业务槽位" },
    { project: "S5590-48UM4YC汇聚", winner: "S5590-48T4XC", vendor: "H3C", tier: "汇聚", spec: "汇聚交换机，交换容量480Gbps，包转发率222Mpps；48个千兆电口，4个万兆光口" },
    { project: "平凉康复-RG-S7805C核心", winner: "S7805C", vendor: "锐捷", tier: "核心", spec: "核心交换机，交换容量230.4Tbps，包转发率38400Mpps；5个业务槽位" },
    { project: "常州职院-RG-S6150-48VS8CQ汇聚", winner: "S6150-48VS8CQ", vendor: "锐捷", tier: "汇聚", spec: "汇聚交换机，交换容量4Tbps，包转发率1012Mpps；48个万兆光口，8个100G QSFP28" },
    { project: "平凉康复-RG-S5310-24GT4XS-P接入", winner: "S5310-24GT4XS-P", vendor: "锐捷", tier: "接入", spec: "接入交换机，交换容量336Gbps，包转发率108Mpps；24个千兆电口，4个万兆光口，支持POE+" },
    // ===== Day 3 (10) =====
    { project: "广东税务-CE9865核心", winner: "CE9865", vendor: "华为", tier: "核心", spec: "数据中心核心交换机，交换容量576Tbps，包转发率288000Mpps；8个业务槽位" },
    { project: "广东税务-CE6881H接入", winner: "CE6881H", vendor: "华为", tier: "接入", spec: "数据中心接入交换机，交换容量12.8Tbps，包转发率8400Mpps；48个25G SFP28，8个100G QSFP28" },
    { project: "苏州疾控-S5735-L48T4XE接入", winner: "S5735-L48T4XE", vendor: "华为", tier: "接入", spec: "接入交换机，交换容量336Gbps，包转发率144Mpps；48个千兆以太网电口，4个万兆以太网光口" },
    { project: "海口监狱-S10508X-G核心", winner: "S10508X", vendor: "H3C", tier: "核心", spec: "核心交换机，交换容量1428Tbps，包转发率460800Mpps；8个业务板卡槽位" },
    { project: "广东省中医院-S6530X汇聚", winner: "S6530X", vendor: "H3C", tier: "汇聚", spec: "汇聚交换机，交换容量6.75Tbps，包转发率4800Mpps；48个万兆光口，6个40G/100G QSFP28" },
    { project: "广东省中医院-S5135S接入", winner: "S5135S", vendor: "H3C", tier: "接入", spec: "接入交换机，交换容量336Gbps，包转发率108Mpps；48个千兆电口，4个万兆光口" },
    { project: "南开大学-S6520X-54HC汇聚", winner: "S6520X-54QC-HI", vendor: "H3C", tier: "汇聚", spec: "汇聚交换机，交换容量4.8Tbps，包转发率2520Mpps；48个万兆光口，4个40/100GE光口" },
    { project: "长沙幼专-S7805C核心", winner: "S7805C", vendor: "锐捷", tier: "核心", spec: "核心交换机，交换容量230.4Tbps，包转发率38400Mpps；5个业务槽位" },
    { project: "长沙幼专-S5310-P接入PoE", winner: "S5310-24GT4XS-P", vendor: "锐捷", tier: "接入", spec: "接入交换机，交换容量336Gbps，包转发率108Mpps；24个千兆电口，4个万兆光口，支持POE" },
    { project: "长沙幼专-S2910-UP接入PoE", winner: "S2910-24GT4SFP-UP-H", vendor: "锐捷", tier: "接入", spec: "接入交换机，交换容量240Gbps，包转发率96Mpps；24个千兆电口，4个千兆光口，支持POE++高功率" },
    // ===== Day 4 (10) =====
    { project: "人行征信-S5735R-S48T4X接入", winner: "S5735", vendor: "华为", tier: "接入", spec: "千兆接入交换机，交换容量336Gbps，包转发率144Mpps；48个10/100/1000BASE-T以太网端口，4个万兆SFP+" },
    { project: "人行征信-S5735-S48S4XE光接入", winner: "S5735-S48S4XE", vendor: "华为", tier: "接入", spec: "千兆光口接入交换机，交换容量336Gbps，包转发率144Mpps；48个千兆SFP光口，4个万兆SFP+" },
    { project: "上海科技大-S5735-S48U4XE-PoE接入", winner: "S5735-S48U4XE", vendor: "华为", tier: "接入", spec: "48口POE接入交换机，交换容量336Gbps，包转发率144Mpps；48个千兆电口，4个万兆光口，支持PoE++" },
    { project: "灵丘县医院-S7506X-G核心", winner: "S7506X-G", vendor: "H3C", tier: "核心", spec: "内网核心交换机，交换容量120Tbps，包转发率72000Mpps；6个业务槽位" },
    { project: "中汇亿达-S5590-48T4XC接入", winner: "S5590-48T4XC", vendor: "H3C", tier: "接入", spec: "千兆接入交换机，交换容量480Gbps，包转发率222Mpps；48个千兆电口，4个万兆光口" },
    { project: "中汇亿达-S6805-56HF数据中心接入", winner: "S6805", vendor: "H3C", tier: "接入", spec: "数据中心万兆接入交换机，交换容量12.8Tbps，包转发率8400Mpps；48个25G SFP28，8个100G QSFP28" },
    { project: "中汇亿达-S10506X-G核心", winner: "S10506X", vendor: "H3C", tier: "核心", spec: "核心交换机，交换容量1428Tbps，包转发率460800Mpps；6个业务槽位" },
    { project: "新田职校-RG-SG7524L核心", winner: "S7524L", vendor: "锐捷", tier: "核心", spec: "核心交换机，交换容量2.4Tbps，包转发率1200Mpps；24个千兆SFP光口，8个万兆SFP+光口" },
    { project: "新田职校-RG-S5760-24SFP4XS-L汇聚", winner: "S5760-24SFP4XS", vendor: "锐捷", tier: "汇聚", spec: "汇聚交换机，交换容量670Gbps，包转发率252Mpps；24个千兆SFP光口，4个万兆SFP+" },
    { project: "交运学校-RG-SF2920-16GT2MG2XS-P全光接入", winner: "SF2920-16GT2MG2XS-P", vendor: "锐捷", tier: "接入", spec: "16口全光POE接入交换机，交换容量240Gbps，包转发率96Mpps；16个千兆电口，2个2.5G光口，2个万兆光口，支持POE" },
    // ===== Day 5 (10) =====
    { project: "长春中医药-S12700E-8核心", winner: "S12700E-8", vendor: "华为", tier: "核心", spec: "核心交换机，交换容量512Tbps，包转发率28800Mpps。8个业务槽位" },
    { project: "长春中医药-S6730-H48X6C-V2汇聚", winner: "S6730-H48X6C", vendor: "华为", tier: "汇聚", spec: "万兆光汇聚交换机，交换容量4.8Tbps，包转发率1440Mpps；48个万兆SFP+接口，6个100G QSFP28接口" },
    { project: "甘肃税务-S5731-H48T4XC接入", winner: "S5731", vendor: "华为", tier: "接入", spec: "千兆接入交换机，交换容量672Gbps，包转发率222Mpps；48个10/100/1000BASE-T以太网端口，4个万兆SFP+" },
    { project: "外交学院-S6526XE汇聚", winner: "S6526XE", vendor: "H3C", tier: "汇聚", spec: "汇聚交换机，交换容量4.8Tbps，包转发率1620Mpps；32个1/10GE SFP+接口，4个40/100GE QSFP28接口" },
    { project: "黑龙江税务-S6520X-54QC-EI汇聚", winner: "S6520X", vendor: "H3C", tier: "汇聚", spec: "万兆汇聚交换机，交换容量4.8Tbps，包转发率2520Mpps；48个万兆光口，6个40G QSFP+接口" },
    { project: "广东省中医院-S5570S-PoE接入", winner: "S5570S", vendor: "H3C", tier: "接入", spec: "POE接入交换机，交换容量688Gbps，包转发率207Mpps；48个千兆以太网电口（支持PoE+），6个万兆SFP+" },
    { project: "中信银行-S6850数据中心接入", winner: "S6850", vendor: "H3C", tier: "接入", spec: "数据中心万兆接入交换机，交换容量12.8Tbps，包转发率8400Mpps；48个25G SFP28接口，8个100G QSFP28接口" },
    { project: "苍梧小学-S7620核心", winner: "S7620", vendor: "锐捷", tier: "核心", spec: "万兆光纤核心交换机，交换容量2.4Tbps，包转发率1200Mpps；20个万兆SFP+光口，2个40G QSFP+口" },
    { project: "哈理工-S6510-48VS8CQ汇聚", winner: "S6510", vendor: "锐捷", tier: "汇聚", spec: "25G数据中心汇聚交换机，交换容量12.8Tbps，包转发率8400Mpps；48个10G/25G SFP28光口，8个100G QSFP28口" },
    { project: "哈理工-S5310-48GT4XS接入", winner: "S5310-48GT4XS", vendor: "锐捷", tier: "接入", spec: "千兆接入交换机，交换容量336Gbps，包转发率108Mpps；48个千兆电口，4个万兆光口" },
    // ===== Day 6 (8) =====
    { project: "财政部-CE6881-48S6CQ数据中心接入", winner: "CE6881", vendor: "华为", tier: "接入", spec: "数据中心万兆接入交换机，48个10G SFP+端口，6个100G QSFP28端口，交换容量4.8Tbps，包转发率2000Mpps" },
    { project: "华西医院-S6850-56HF数据中心25G接入", winner: "S6850", vendor: "H3C", tier: "接入", spec: "数据中心25G服务器接入交换机，48个25G SFP28端口，8个100G QSFP28端口，交换容量3.2Tbps，包转发率2560Mpps" },
    { project: "海关中卫-S9820-8C-G汇聚", winner: "S9820-8C-G", vendor: "H3C", tier: "汇聚", spec: "数据中心汇聚交换机，8插卡槽位，交换容量25.6Tbps，包转发率8000Mpps" },
    { project: "海关中卫-S12504G-AF核心", winner: "S12504G", vendor: "H3C", tier: "核心", spec: "数据中心核心交换机，交换容量336Tbps，包转发率115200Mpps；4个业务槽位" },
    { project: "牡丹江医院-S9820-8C核心", winner: "S9820", vendor: "H3C", tier: "核心", spec: "AI集群核心交换机，8个业务插卡槽位，交换容量25.6Tbps，包转发率8000Mpps" },
    { project: "华西医院-S5735-S48T4XE园区接入", winner: "S5735", vendor: "华为", tier: "接入", spec: "园区千兆接入交换机，交换容量336Gbps，包转发率144Mpps；48个千兆电口，4个万兆SFP+" },
    { project: "吉林税务-S6850-56HF 25G接入", winner: "S6850", vendor: "H3C", tier: "接入", spec: "25G接入交换机，48个25G SFP28端口，8个100G QSFP28端口，交换容量3.2Tbps，包转发率2560Mpps" },
    { project: "台州公安-S6805-54HF数据中心接入", winner: "S6805", vendor: "H3C", tier: "接入", spec: "数据中心万兆服务器接入交换机，48个10G SFP+端口，6个100G QSFP28端口，交换容量2.56Tbps，包转发率1600Mpps" },
    // ===== Day 7 新增 (7) =====
    { project: "西双版纳州一中-S8700-6核心", winner: "S8700", vendor: "华为", tier: "核心", spec: "核心交换机，交换容量336Tbps，包转发率230400Mpps；6个业务槽位，双主控双电源" },
    { project: "昆明学院-S10508X-G核心", winner: "S10508X", vendor: "H3C", tier: "核心", spec: "核心交换机，交换容量1428Tbps，包转发率460800Mpps；8个业务板卡槽位" },
    { project: "昆明学院-S6550X-32Q-HI汇聚", winner: "S6550X-32Q-HI", vendor: "H3C", tier: "汇聚", spec: "100G汇聚交换机，32个40/100GE QSFP28端口，交换容量48Tbps，包转发率2800Mpps" },
    { project: "昆明学院-S5590-28T8XC-EI接入", winner: "S5590-28T8XC-EI", vendor: "H3C", tier: "接入", spec: "接入交换机，28个千兆电口，8个万兆SFP+端口，交换容量2.4Tbps，包转发率672Mpps" },
    { project: "昆明学院-S6520X-30QCEI机房汇聚", winner: "S6520X-30QC-EI", vendor: "H3C", tier: "汇聚", spec: "机房汇聚交换机，24个万兆SFP+端口，2个40G QSFP+端口，交换容量2.56Tbps，包转发率720Mpps" },
    { project: "南平学院-RG-S6150-48VS8CQ-X SDN汇聚", winner: "S6150-48VS8CQ-X", vendor: "锐捷", tier: "汇聚", spec: "SDN汇聚交换机，交换容量4Tbps，包转发率1012Mpps；48个25G SFP28光口，8个100G QSFP28口" },
    { project: "临沧公安-S6520X-54XG-EI-G汇聚", winner: "S6520X-54XG-EI", vendor: "H3C", tier: "汇聚", spec: "万兆汇聚交换机，交换容量4.8Tbps，包转发率2520Mpps；48个万兆光口，6个40G QSFP+接口" },
    // ===== Day 8 新增 (8) =====
    { project: "浙江大学-S6730-H48X6C-V2汇聚", winner: "S6730-H48X6C", vendor: "华为", tier: "汇聚", spec: "汇聚交换机，48个万兆SFP+，6个100G QSFP28，交换容量4.8Tbps，包转发率1440Mpps" },
    { project: "吉林医药学院-S10506X核心", winner: "S10506X", vendor: "H3C", tier: "核心", spec: "核心交换机，交换容量1428Tbps，包转发率460800Mpps；6个业务槽位" },
    { project: "吉林医药学院-S7503X汇聚", winner: "S7503X", vendor: "H3C", tier: "汇聚", spec: "汇聚交换机，交换容量2.88Tbps，包转发率2160Mpps；3个业务槽位" },
    { project: "吉林医药学院-S5130S-PoE接入", winner: "S5130S", vendor: "H3C", tier: "接入", spec: "PoE接入交换机，24个千兆电口(PoE)，4个千兆光口，交换容量336Gbps，包转发率108Mpps" },
    { project: "华西医院2025-S8700-6园区汇聚", winner: "S8700", vendor: "华为", tier: "核心", spec: "园区汇聚交换机，交换容量336Tbps，包转发率230400Mpps；6个业务槽位" },
    { project: "华西医院2025-S5735-S48T4XE接入", winner: "S5735-S48T4XE", vendor: "华为", tier: "接入", spec: "接入交换机，48个千兆电口，4个万兆光口，交换容量224Gbps，包转发率168Mpps" },
    { project: "华西医院2025-S6850-56HF数据中心接入", winner: "S6850", vendor: "H3C", tier: "接入", spec: "数据中心25G接入交换机，48个25G SFP28端口，8个100G QSFP28端口，交换容量3.2Tbps，包转发率2560Mpps" },
    { project: "吉林医药学院-S5755-H48T4Y2CZ接入", winner: "S5755", vendor: "华为", tier: "接入", spec: "高品质接入交换机，48个千兆电口，4个25G光口，2个100G光口，交换容量2.56Tbps，包转发率822Mpps" },
];

let hitTop1 = 0, hitTop3 = 0, hitTop5 = 0;
let validCases = 0;
let results = [];

for (const c of allCases) {
    const req = parseRequirement(c.spec);
    let scored = allSwitches.map(sw => ({
        model: sw.model, vendor: sw.vendor, tier: sw.tier,
        score: calcMatchScore(sw, req)
    })).sort((a, b) => b.score - a.score);
    
    const winnerKey = c.winner.toLowerCase().replace(/[-_]/g, '').substring(0, 6);
    let rank = -1;
    for (let i = 0; i < scored.length; i++) {
        const mk = scored[i].model.toLowerCase().replace(/[-_]/g, '');
        if (mk.includes(winnerKey)) { rank = i; break; }
    }
    
    const found = rank >= 0;
    if (found) {
        validCases++;
        if (rank < 1) hitTop1++;
        if (rank < 3) hitTop3++;
        if (rank < 5) hitTop5++;
    }
    
    results.push({
        project: c.project, winner: c.winner, vendor: c.vendor, tier: c.tier,
        rank: found ? rank + 1 : '未找到',
        score: found ? scored[rank].score : 0,
        top5: found && rank < 5, top3: found && rank < 3, top1: found && rank < 1,
    });
}

console.log("=".repeat(70));
console.log("Day 9 数据修复后测试（73案例）");
console.log("=".repeat(70));
console.log(`总案例：${allCases.length}个，数据库：${allSwitches.length}款`);
console.log(`有效案例：${validCases}个`);

// 按层级
console.log("\n按层级统计：");
for (const tier of ['核心', '汇聚', '接入']) {
    const tierResults = results.filter(r => r.tier === tier && r.rank !== '未找到');
    const top5 = tierResults.filter(r => r.top5).length;
    const top3 = tierResults.filter(r => r.top3).length;
    const top1 = tierResults.filter(r => r.top1).length;
    console.log(`  ${tier}层: ${tierResults.length}个, Top1=${top1}(${Math.round(top1/tierResults.length*100)}%), Top3=${top3}(${Math.round(top3/tierResults.length*100)}%), Top5=${top5}(${Math.round(top5/tierResults.length*100)}%)`);
}

// 按厂商
console.log("\n按厂商统计：");
for (const vendor of ['华为', 'H3C', '锐捷']) {
    const vResults = results.filter(r => r.vendor === vendor && r.rank !== '未找到');
    const top5 = vResults.filter(r => r.top5).length;
    const top3 = vResults.filter(r => r.top3).length;
    const top1 = vResults.filter(r => r.top1).length;
    console.log(`  ${vendor}: ${vResults.length}个, Top1=${top1}(${Math.round(top1/vResults.length*100)}%), Top3=${top3}(${Math.round(top3/vResults.length*100)}%), Top5=${top5}(${Math.round(top5/vResults.length*100)}%)`);
}

console.log("\n" + "=".repeat(70));
console.log(`总体命中率:`);
console.log(`  Top 1: ${hitTop1}/${validCases} (${Math.round(hitTop1/validCases*100)}%)`);
console.log(`  Top 3: ${hitTop3}/${validCases} (${Math.round(hitTop3/validCases*100)}%)`);
console.log(`  Top 5: ${hitTop5}/${validCases} (${Math.round(hitTop5/validCases*100)}%)`);
console.log("=".repeat(70));

console.log("\n未进入Top5的案例：");
const missed = results.filter(r => r.rank !== '未找到' && !r.top5);
missed.forEach((r, i) => {
    console.log(`  ${i+1}. ${r.project} - 第${r.rank}名 (${r.vendor}/${r.tier}) 分数:${r.score}`);
});

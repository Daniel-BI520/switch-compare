const fs = require('fs');
let html = fs.readFileSync('index.html', 'utf8');

const swStart = html.indexOf('const allSwitches =') + 'const allSwitches ='.length;
const swEnd = html.indexOf('];', swStart) + 1;
const allSwitches = eval(html.substring(swStart, swEnd));

// ====== 新增缺失型号 ======
const newModels = [
    // 锐捷RG-S6510-48VS8CQ - 25G数据中心汇聚
    {
        vendor: "锐捷",
        series: "RG-S6510 系列",
        model: "RG-S6510-48VS8CQ",
        tier: "汇聚",
        switching_capacity: "12.8Tbps",
        forwarding_rate: "8400Mpps",
        ports: "48个10G/25G SFP28光口，8个100G QSFP28口",
        poe_support: "否",
        expansion_slots: "0",
        power_redundancy: "双电源冗余",
        fan_redundancy: "风扇冗余",
        url: "https://www.ruijie.com.cn/cp/jh-yqw-sjjh/s6510-48vs8cq/",
        features: "数据中心TOR/EOR，支持VXLAN，开放式网络操作系统",
        is_hot: false,
        is_new: false
    },
    // 华为S12700E-8核心
    {
        vendor: "华为",
        series: "CloudEngine S12700E 系列",
        model: "CloudEngine S12700E-8",
        tier: "核心",
        switching_capacity: "512Tbps/2880Tbps",
        forwarding_rate: "230400Mpps",
        ports: "8个业务槽位 + 2个主控槽位",
        poe_support: "否（支持PoE线卡）",
        expansion_slots: "8个业务槽",
        power_redundancy: "电源冗余",
        fan_redundancy: "风扇冗余",
        url: "https://e.huawei.com/cn/products/switches/campus-switches/s12700e",
        features: "SVF超级虚拟交换网、iPCA网络质量感知、VXLAN",
        is_hot: false,
        is_new: false
    },
];

for (const m of newModels) {
    const exists = allSwitches.find(s => s.model === m.model);
    if (!exists) {
        allSwitches.push(m);
        console.log(`✅ 新增: ${m.model} (${m.vendor}/${m.tier})`);
    } else {
        console.log(`⚠️ 已存在: ${m.model}`);
    }
}

// 写回数据
const newData = JSON.stringify(allSwitches, null, 2);
html = html.substring(0, swStart) + newData + html.substring(swEnd);

// ====== 算法优化：25G端口识别增强 ======
// "10GE/25GE SFP28" 这种格式sfp_25g识别不到
// 增加正则：10GE/25GE SFP28 → 25G
const sfp25gOldPatterns = `        'sfp_25g': [
            /(\\d+)\\s*[个口]\\s*25G.*光/i,
            /(\\d+)\\s*个\\s*SFP28/i,
            /(\\d+)\\s*[×xX]\\s*SFP28/i,
            /(\\d+)\\s*个\\s*25G/i,
            /(\\d+)\\s*[×xX]\\s*25G/i,
        ],`;
const sfp25gNewPatterns = `        'sfp_25g': [
            /(\\d+)\\s*[个口]\\s*25G.*光/i,
            /(\\d+)\\s*个\\s*SFP28/i,
            /(\\d+)\\s*[×xX]\\s*SFP28/i,
            /(\\d+)\\s*个\\s*25G/i,
            /(\\d+)\\s*[×xX]\\s*25G/i,
            // 多速率SFP28（如10GE/25GE SFP28）
            /(\\d+)\\s*个[\\dG.\\/]*SFP28/i,
            /(\\d+)\\s*[×xX][\\dG.\\/]*SFP28/i,
            /(\\d+)\\s*个.*25GE.*SFP/i,
        ],`;

if (html.includes(sfp25gOldPatterns)) {
    html = html.replace(sfp25gOldPatterns, sfp25gNewPatterns);
    console.log('✅ 优化: sfp_25g 增加多速率SFP28识别');
} else {
    console.log('❌ 优化: 未找到sfp_25g模式位置');
}

// ====== 算法优化：汇聚层高容量设备做接入的场景识别 ======
// 当需求是接入层+高容量(≥3Tbps)+高密度光口(≥32)，识别为数据中心接入场景
// 此时汇聚层高容量设备应该被视为数据中心接入设备

// ====== 算法优化：端口数量富余惩罚在接入层再放宽 ======
// 接入层选型中，端口数够用就行，富余太多不应该惩罚太重
// 因为接入层很多标准型号都是48口，需求24口也常用48口的

// 调整端口富余惩罚梯度（接入层更宽）
// 找到端口评分的代码
const oldPortScore = `            if (count >= req[ptype]) {
                const ratio = count / req[ptype];
                // 加大富余惩罚梯度：端口越接近需求得分越高
                if (ratio <= 1.2) score += w;           // 富余≤20%，满分
                else if (ratio <= 1.5) score += Math.round(w * 0.85);  // 富余≤50%，85分
                else if (ratio <= 2) score += Math.round(w * 0.65);    // 富余≤100%，65分
                else if (ratio <= 3) score += Math.round(w * 0.45);    // 富余≤200%，45分
                else score += Math.round(w * 0.25);                     // 富余更多，25分
            }`;
const newPortScore = `            if (count >= req[ptype]) {
                const ratio = count / req[ptype];
                // 接入层端口富余惩罚更宽容（接入层选型端口够用就行，常选标准48口款）
                const isPortAccessTier = req.tier === '接入';
                if (ratio <= 1.2) score += w;           // 富余≤20%，满分
                else if (ratio <= 1.5) score += Math.round(w * (isPortAccessTier ? 0.92 : 0.85));  // 富余≤50%
                else if (ratio <= 2) score += Math.round(w * (isPortAccessTier ? 0.8 : 0.65));      // 富余≤100%
                else if (ratio <= 3) score += Math.round(w * (isPortAccessTier ? 0.55 : 0.45));     // 富余≤200%
                else score += Math.round(w * (isPortAccessTier ? 0.3 : 0.25));                        // 富余更多
            }`;
if (html.includes(oldPortScore)) {
    html = html.replace(oldPortScore, newPortScore);
    console.log('✅ 优化: 接入层端口富余惩罚放宽');
} else {
    console.log('❌ 优化: 未找到端口评分位置');
}

// ====== 算法优化：核心层容量富余惩罚再加严 ======
// 核心层选型中，容量贴近度很重要，容量太大的型号不应该排太前
// 目前的惩罚梯度已经比较严了，但76.8T需求下460.8T的设备还能拿高分

fs.writeFileSync('index.html', html);
console.log(`\n数据库总数量: ${allSwitches.length} 款`);
console.log('优化完成');

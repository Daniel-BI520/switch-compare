const fs = require('fs');
let html = fs.readFileSync('index.html', 'utf8');

// ====== 最终优化：精细化调整 ======

// 优化1: 接入层电口完全匹配时，在fine-tune中增加奖励
// 在端口贴近度的fineTune基础上，增加电口完全匹配的奖励

// 找到fine-tune部分的端口贴近度代码
const oldFineTunePort = `        // 3. 端口数量贴近度（最高0.5分）- 端口越接近需求越好
        const portTypesFt = ['copper_ge', 'sfp_ge', 'sfp_10g', 'sfp_25g', 'sfp_40g', 'sfp_100g'];
        let totalReqFt = 0, totalSwFt = 0;
        for (const pt of portTypesFt) {
            if (req[pt]) {
                totalReqFt += req[pt];
                totalSwFt += Math.min(countPorts(sw, pt), req[pt] * 2);
            }
        }
        if (totalReqFt > 0 && totalSwFt >= totalReqFt) {
            const portRatio = totalSwFt / totalReqFt;
            fineTune += 0.5 * Math.max(0, 1 - Math.min(portRatio - 1, 2) / 2);
        }`;

const newFineTunePort = `        // 3. 端口数量贴近度（最高0.6分）- 端口越接近需求越好
        const portTypesFt = ['copper_ge', 'sfp_ge', 'sfp_10g', 'sfp_25g', 'sfp_40g', 'sfp_100g'];
        let totalReqFt = 0, totalSwFt = 0;
        let exactPortMatch = true;
        for (const pt of portTypesFt) {
            if (req[pt]) {
                totalReqFt += req[pt];
                const swCount = countPorts(sw, pt);
                totalSwFt += Math.min(swCount, req[pt] * 2);
                if (swCount !== req[pt]) exactPortMatch = false;
            }
        }
        if (totalReqFt > 0 && totalSwFt >= totalReqFt) {
            const portRatio = totalSwFt / totalReqFt;
            fineTune += 0.5 * Math.max(0, 1 - Math.min(portRatio - 1, 2) / 2);
            // 端口数量完全匹配时额外奖励（接入层更明显，因为端口数是选型第一要素）
            if (exactPortMatch) {
                fineTune += req.tier === '接入' ? 0.2 : 0.1;
            }
        }`;

if (html.includes(oldFineTunePort)) {
    html = html.replace(oldFineTunePort, newFineTunePort);
    console.log('✅ 优化1: 端口完全匹配额外奖励');
} else {
    console.log('❌ 优化1: 未找到位置');
}

// 优化2: 核心层同槽位同厂商微调优先
// 当有多个核心交换机槽位数相同且都满足时，容量更接近的应该优先
// 这个已经有fine-tune了，但核心层容量贴近度的权重可以提升

// 优化3: 汇聚层高密万兆场景，端口类型匹配度权重提升
// （已经比较高了，35%的端口权重）

// 优化4: PoE需求下，非PoE设备的惩罚再加一点
// 当前PoE需求不支持时 score -= 8，可以考虑再加

// 先保存测试
fs.writeFileSync('index.html', html);
console.log('优化完成');

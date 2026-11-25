# 交换机对比工具更新报告 2026-11-26

## 执行概要
- **策略**：核心参数优先校验 + 疑点深挖（轻量防反扒）
- **数据规模**：共 522 款（锐捷 100 / 华为 188 / H3C 234）
- **总变更**：新增 0 款 / 参数更新 0 款 / 下架 0 款 / URL修复 0 款 / 数据规范修正 1 款
- **本轮核心动作**：17 款热门型号全量核验 + 3 款抽样抽查，全部与官网CN一致；修正 S6550X-54H-HI 字段结构并补标"新"标签

## 一、热门型号核验（17款全部一致 ✅）
| 厂商 | 型号 | 交换容量 | 包转发率 | 核验结果 |
|---|---|---|---|---|
| 华为 | CE8855-32CQ4BQ | 8Tbps/128Tbps | 2400Mpps | ✅ 官网CN一致 |
| 华为 | S6730-H24X6C-V2 | 4.8Tbps/48Tbps | 1620Mpps | ✅ 官网CN一致 |
| 华为 | CE6881E-48S6CQ | 2.88Tbps | 940Mpps | ✅ 官网CN一致 |
| 华为 | CE6881-48S6CQ | 4.8Tbps/96Tbps | 2000Mpps | ✅ 官网CN一致 |
| 华为 | S5735-S48T4XEZ-V2 | 1.36Tbps/13.6Tbps | 327Mpps/770Mpps | ✅ 官网CN一致 |
| 华为 | S5735-L24P4S-A-V2 | 672Gbps/6.72Tbps | 171Mpps | ✅ 官网CN一致 |
| H3C | S10506X | 1071Tbps/3213Tbps | 345600Mpps | ✅ 官网CN一致 |
| H3C | S7506X-G | 102.4Tbps/460.8Tbps | 76800Mpps | ✅ 官网CN一致 |
| H3C | S5560S-28F-EI | 1.28Tbps/12.8Tbps | 228Mpps | ✅ 官网CN一致 |
| H3C | S5590-28S8XC-HI | 2.56Tbps/25.6Tbps | 660Mpps/930Mpps | ✅ 官网CN一致 |
| H3C | S5590-48T4XC-EI | 2.4Tbps/24Tbps | 672Mpps | ✅ 官网CN一致 |
| H3C | S6520X-54HC-EI | 2.56Tbps/25.6Tbps | 1620Mpps | ✅ 官网CN一致 |
| H3C | S6530X-48X8C | 8Tbps/80Tbps | 2000Mpps | ✅ 官网CN一致 |
| H3C | S6530X-48Y8C | 8Tbps/80Tbps | 3000Mpps | ✅ 官网CN一致 |
| H3C | S5130S-28P-PWR-EI | 672Gbps/6.72Tbps | 126Mpps | ✅ 官网CN一致（上轮已同步672G） |
| H3C | S5130S-48UN6X-EI-G-V2 | 1.36Tbps/13.6Tbps | 327Mpps/770Mpps | ✅ 官网CN一致 |
| H3C | S6850-56HF | 8Tbps/128Tbps | 2400Mpps | ✅ 官网CN一致 |

## 二、抽样抽查（非热门，3款全部一致 ✅）
- 华为 CE6857F-48S6CQ：4.8Tbs/96Tbps + 2000Mpps ✅（CE6800系列页）
- H3C S6520X-30QC-EI：2.56Tbps/25.6Tbps + 720Mpps/1260Mpps ✅（官网CN）
- 锐捷 RG-S5760C-24GT8XS-X：2.56Tbps/25.6Tbps + 660Mpps/930Mpps ✅（中文官网独立页）

## 三、数据规范修正（1款）
**H3C S6550X-54H-HI**（汇聚，全光多通道以太光交换机）：
- 官网核验：交换容量 48Tbps / 包转发率 9600Mpps / 54×40-100G QSFP28 + 2×10G SFP+，与库中一致 ✅
- **字段结构修正**：原为旧字段结构（level/poe/extended_slots/release_date 布尔型），已标准化为全库统一结构（tier/poe_support/expansion_slots/power_redundancy/fan_redundancy）
- **标签更新**：官网2026-04-24发布（≤12个月），补标 is_new=true；同时清理冗余 release_date 字段
- URL 保持不变（H3C 官网CN独立产品页，有效 ✅）

## 四、新型号排查（新增0款）
- 锐捷 RG-S6503-48VS8CQ（2026-07发布）：中文官网无独立产品页（URL 404，仅彩页PDF），按URL红线不入库
- 锐捷 RG-S6990-64OC2XS / RG-S6990-128QC2XS：中文官网暂无独立产品页，不入库
- H3C 2026 新品 S9828-64FP / S9828-128EO / S12500R-64EP 等：AI智算互联产品，不在入库范围
- 华为 2026 新品以全光/工业交换机为主（S5755I-H系列工业交换机、Twins 400G），不在核心/汇聚/接入常规范围，不入库

## 五、URL质量
- 全库 522 款：0 条空 URL、0 条第三方链接
- 本轮无 URL 变更（无新增/无失效）

## 六、标签状态
- 热门标签：17 款保持不变（华为6 + H3C11）
- 新型号标签：H3C 1 款（S6550X-54H-HI，2026-04发布标"新"）；华为 0 款
- 锐捷不标标签（惯例）

## 七、后续同步
- switch_data_normalized.json 已更新（update_time=2026-11-26）
- index.html switchData / allSwitches / updateTime / 页面显示时间 已同步
- Git 提交 + GitHub Pages 推送（Daniel-BI520/switch-compare）
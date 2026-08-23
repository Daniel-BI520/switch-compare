# 交换机参数双日更新报告

**更新日期：** 2026-08-24
**数据总量：** 485款（锐捷94 / 华为170 / H3C 221）
**校验方式：** 核心参数抽样校验（系列代表型号搜索snippet比对 + 差异型号官网详情页fetch_web核实）
**抽样覆盖：** 9款代表型号（华为3+H3C 3+锐捷3）+ 9款数据中心/高端系列（华为3+H3C 3+锐捷3）

## 一、参数修正明细（共10款）

### 1. 锐捷 RG-S5310-E 系列（4款）— 交换容量提升3-4倍
| 型号 | 修正前交换容量 | 修正后交换容量 | 修正前包转发率 | 修正后包转发率 |
|------|--------------|--------------|--------------|--------------|
| RG-S5310-24GT4XS-E | 336Gbps/3.36Tbps | **1.36Tbps/13.6Tbps** | 95.23Mpps/126Mpps | **291Mpps/770Mpps** |
| RG-S5310-24GT4XS-P-E | 336Gbps/3.36Tbps | **1.36Tbps/13.6Tbps** | 95.23Mpps/126Mpps | **291Mpps/770Mpps** |
| RG-S5310-48GT4XS-E | 432Gbps/4.32Tbps | **1.36Tbps/13.6Tbps** | 130.95Mpps/166Mpps | **560Mpps/770Mpps** |
| RG-S5310-48SFP4XS-E | 432Gbps/4.32Tbps | **1.36Tbps/13.6Tbps** | 196Mpps/222Mpps | **560Mpps/770Mpps** |

**来源：** 锐捷官网 S5310-24GT4XS-E 产品页 https://www.ruijie.com.cn/cp/jh-yqw-jrjh/s531024gt4xse/

### 2. H3C S5560S-EI 系列（5款）— 交换容量提升2.5倍
| 型号 | 修正前交换容量 | 修正后交换容量 | 修正前包转发率 | 修正后包转发率 |
|------|--------------|--------------|--------------|--------------|
| S5560S-28P-EI | 336Gbps/3.36Tbps | **826Gbps/8.26Tbps** | 108Mpps/126Mpps | **126Mpps** |
| S5560S-52P-EI | 336Gbps/3.36Tbps | **826Gbps/8.26Tbps** | 132Mpps/166Mpps | **166Mpps** |
| S5560S-28S-PWR-EI | 336Gbps/3.36Tbps | **826Gbps/8.26Tbps** | 108Mpps/126Mpps | **228Mpps** |
| S5560S-52S-PWR-EI | 336Gbps/3.36Tbps | **826Gbps/8.26Tbps** | 132Mpps/166Mpps | **264Mpps** |
| S5560S-28F-EI | 336Gbps/3.36Tbps | **1.28Tbps/12.8Tbps** | 126Mpps | **228Mpps** |

**来源：** H3C官网 S5560S-EI 系列产品页 https://wwwsg.h3c.com/cn/Products_And_Solution/InterConnect/Products/Switches/Products/Park_Switches/Aggregation_Switch/S5500/S5560S-EI/

> 备注：S5560S-28S-EI、S5560S-52S-EI 两款参数与官网一致（1.28Tbps/12.8Tbps），无需修改。S5560S-52F-EI 官网上有该型号但当前库中暂无，后续评估是否新增。

### 3. H3C S7506X-G（1款）— 高端框式参数修正
| 型号 | 修正前交换容量 | 修正后交换容量 | 修正前包转发率 | 修正后包转发率 |
|------|--------------|--------------|--------------|--------------|
| S7506X-G | 76.8Tbps/336Tbps | **102.4Tbps/460.8Tbps** | 8640Mpps/57600Mpps | **76800Mpps** |

**来源：** H3C官网 S7500X-G 系列产品页 https://wwwsg.h3c.com/cn/Products_And_Solution/InterConnect/Products/Switches/Products/Data_Center_Switch/Aggregation_Switch/S7500X/S7500X-G/

## 二、已核实无需修改的型号（9+系列）

### 华为（3系列）
- CloudEngine S6750-H36C / S6750-H48Y8C：8Tbps/80Tbps，与官网一致 ✅
- CloudEngine S12700H-4 / S12700H-8：952/2876Tbps / 1904/5752Tbps，与官网一致 ✅
- CE16800-X 系列：953Tbps~3813Tbps，与官网一致 ✅

### H3C 数据中心（3系列）
- S6850系列（6款）：8Tbps/128Tbps，与官网一致 ✅
- S9820系列（4款）：12.8Tbps/204.8Tbps ~ 25.6Tbps，与官网一致 ✅
- S6850-56HF（老款）：3.2Tbps/2560Mpps，独立型号保留 ✅

### 锐捷数据中心（3系列）
- RG-S6231系列（2款）：4.8Tbps/96Tbps，与官网一致 ✅
- RG-S6990系列（3款）：102.4Tbps，与官网一致 ✅
- RG-N18010-X：待进一步核实（疑似数据异常偏高） ⚠️

## 三、待跟进事项

1. **锐捷 RG-N18010-X 参数存疑**：现有数据显示 1607Tbps/4821Tbps, 460800Mpps，与官网各来源（230T/516T、153.6T等）差异巨大，疑似早期录入错误或混淆了其他型号。需专门核实。

2. **S5560S-52F-EI 缺失**：官网 S5560S-EI 系列包含 8 款型号，当前库中缺 S5560S-52F-EI，下次更新时评估新增。

3. **URL域名切换**：H3C 部分型号URL从 www.h3c.com 切至 wwwsg.h3c.com（官网独立产品页），已同步更新。

## 四、数据统计

| 指标 | 数值 |
|------|------|
| 总型号数 | 485 |
| 锐捷 | 94 |
| 华为 | 170 |
| H3C | 221 |
| 本次参数修正 | 10款 |
| 抽样校验覆盖 | 18款（跨9+系列） |
| 详情页访问量 | 5个URL（约28%抽样访问率） |

---
*报告生成时间：2026-08-24*
*数据源：锐捷 ruijie.com.cn / 华为 huawei.com / H3C h3c.com 官网产品页*

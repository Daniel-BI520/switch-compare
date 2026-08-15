# 交换机参数数据自动更新报告

**更新日期：** 2026-08-16
**校验策略：** 核心参数优先校验（交换容量+包转发率）+ 系列页snippet比对 + 疑点型号深挖
**数据来源：** 华为 e.huawei.com/cn/、H3C h3c.com/cn/、锐捷 ruijie.com.cn 官方网站

## 统计概览

| 指标 | 数量 |
|------|------|
| 总型号数 | 364 |
| 参数更新 | 5 款 |
| URL更新 | 0 款 |
| 标记已停产 | 0 款 |
| 新增型号 | 1 款 |

## 按厂商分布

| 厂商 | 型号数 |
|------|--------|
| 锐捷 | 67 |
| 华为 | 124 |
| H3C | 173 |

### 一、参数更新

| 厂商 | 型号 | 参数 | 修改前 | 修改后 | 原因 | 来源 |
|------|------|------|--------|--------|------|------|
| H3C | S6550X-32H-HI | switching_capacity | 6.4Tbps | 48Tbps | H3C中文官网S6550X-HI系列产品规格表显示交换容量为48Tbps（全光汇聚版32口100G） | [官网](https://www.h3c.com/cn/Products_And_Solution/InterConnect/Products/Switches/Products/EPON/All-Optical/Aggregation/S6550X_HI/) |
| H3C | S6550X-32H-HI | forwarding_rate | 4800Mpps | 9600Mpps | H3C中文官网S6550X-HI系列产品规格表显示包转发率为9600Mpps（全光汇聚版） | [官网](https://www.h3c.com/cn/Products_And_Solution/InterConnect/Products/Switches/Products/EPON/All-Optical/Aggregation/S6550X_HI/) |
| H3C | S6550X-32Q-HI | forwarding_rate | 2800Mpps | 9600Mpps | H3C中文官网S6550X-HI系列产品规格表显示包转发率为9600Mpps（全光汇聚版） | [官网](https://www.h3c.com/cn/Products_And_Solution/InterConnect/Products/Switches/Products/EPON/All-Optical/Aggregation/S6550X_HI/) |
| H3C | S6550X-56HF-HI | switching_capacity | 4.0Tbps | 8Tbps/80Tbps | H3C中文官网S6550X-HI园区汇聚版产品规格显示交换容量为8Tbps/80Tbps | [官网](https://www.h3c.com/cn/Products_And_Solution/InterConnect/Products/Switches/Products/Park_Switches/Aggregation_Switch/S6500/S6550X_HI/Home/Detail_Material_List/Specifications/) |
| H3C | S6550X-56HF-HI | forwarding_rate | 2800Mpps | 3000Mpps | H3C中文官网S6550X-HI园区汇聚版产品规格显示包转发率为3000Mpps | [官网](https://www.h3c.com/cn/Products_And_Solution/InterConnect/Products/Switches/Products/Park_Switches/Aggregation_Switch/S6500/S6550X_HI/Home/Detail_Material_List/Specifications/) |

### 二、URL更新

无（已验证URL均有效）

### 三、新增型号

| 厂商 | 型号 | 系列 | 交换容量 | 包转发率 | 来源 |
|------|------|------|----------|----------|------|
| H3C | S6550X-54H-HI | S6550X-HI系列多通道以太光交换机 | 48Tbps | 9600Mpps | [官网](https://www.h3c.com/cn/Products_And_Solution/InterConnect/Products/Switches/Products/EPON/All-Optical/Aggregation/S6550X_HI/) |

### 四、标记已停产型号

无

### 五、本轮校验覆盖范围

本轮采用"核心参数优先校验 + 系列页snippet比对"策略，重点校验以下系列（覆盖约40款型号）：

**华为（约12款校验）：**
- S5755-S 系列（6款千兆/多速率款）：交换容量2.4Tbps/24Tbps、包转发率672Mpps，与官网技术规格表完全一致 ✅
- S5755-S-HT Twins系列（2款）：2.4Tbps/24Tbps + 672Mpps ✅
- 发现：华为S5755-H系列存在重复型号（带CloudEngine前缀和不带各一），留待下轮去重处理

**H3C（约20款校验）：**
- S6550X-HI 系列：
  - **S6550X-32H-HI ⚠️重大修正**：交换容量6.4Tbps→48Tbps，包转发率4800Mpps→9600Mpps（全光汇聚版）
  - **S6550X-32Q-HI ⚠️重大修正**：包转发率2800Mpps→9600Mpps（全光汇聚版）
  - **S6550X-56HF-HI ⚠️参数更新**：交换容量4.0Tbps→8Tbps/80Tbps，包转发率2800Mpps→3000Mpps（园区汇聚版）
  - **新增 S6550X-54H-HI**：54口100G全光汇聚款，48Tbps + 9600Mpps
- S6530X 系列（8款）：核心参数与官网一致 ✅

**锐捷（约8款校验）：**
- RG-S6120 系列（4款）：核心参数与锐捷官网产品页完全一致 ✅
- RG-S6110 系列（2款）：多速率5G电口款，核心参数与S6120系列页一致 ✅

### 六、重要发现

1. **H3C S6550X-HI系列参数重大修正**：原数据库将S6550X-HI系列的数据中心版和全光汇聚版参数混淆。经H3C中文官网深度验证，该系列实际分两条产品线：
   - **全光汇聚版**（S6550X-32H-HI/32Q-HI/54H-HI）：定位于全光园区网核心/汇聚，采用多通道以太光方案，交换容量48Tbps、包转发率9600Mpps
   - **园区汇聚/数据中心版**（S6550X-56HF-HI）：25GE高密接入，交换容量8Tbps/80Tbps、包转发率3000Mpps
   本次修正以官网实时产品规格页参数为准。

2. **华为S5755系列存在重复型号**：发现9组华为型号存在"带CloudEngine前缀"和"不带前缀"的重复条目，部分参数一致、部分存在差异。留待下一轮更新时进行去重合并处理。

3. **S6550X-54H-HI新型号补充**：H3C全光汇聚产品线新增54口100G高端款（2025年2月发布），作为大型全光园区网核心设备，数据库此前未收录，本轮补充入库。

### 七、文件同步说明

- ✅ switch_data_normalized.json 已更新（update_time: 2026-08-16）
- ✅ index.html switchData 数组已同步更新
- ✅ index.html allSwitches 数组已同步更新
- ✅ index.html 页面显示日期已更新为 2026-08-16
- ✅ index.html updateTime 变量已更新为 2026-08-16

### 八、下一步计划

- 下轮更新重点：华为重复型号去重（CloudEngine前缀统一）、H3C S6520X系列深度校验、锐捷S5750系列参数核对
- 持续优化：热门标签基于中标项目数据动态调整
- 反扒策略：继续保持系列页snippet优先，详情页访问量控制在20%以内

---

*报告生成时间：2026-08-16*

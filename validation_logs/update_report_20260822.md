# 交换机参数数据自动更新报告

**更新日期：** 2026-08-22
**校验策略：** 核心参数优先校验（交换容量+包转发率）+ 系列页snippet比对 + 疑点型号深挖
**数据来源：** 华为 e.huawei.com/cn/、H3C h3c.com/cn/、锐捷 ruijie.com.cn 官方网站

## 统计概览

| 指标 | 数量 |
|------|------|
| 总型号数 | 485 |
| 参数更新 | 32 项（涉及 19 款型号） |
| URL更新 | 0 款 |
| 新增型号 | 1 款 |
| 移除重复 | 1 款 |
| 标记已停产 | 0 款 |

## 按厂商分布

| 厂商 | 型号数 | 参数更新 | 新增 | 去重 |
|------|--------|----------|------|------|
| 锐捷 | 94 | 0 | 0 | 0 |
| 华为 | 170 → 170 | 4 | 1 | 1 |
| H3C | 221 | 28 | 0 | 0 |

## 一、参数更新明细

### 1.1 华为S5731-H系列（重大修正，4项 / 2款）

数据来源：[华为企业业务官网 - CloudEngine S5731-H系列](https://e.huawei.com/cn/products/switches/campus-switches/s5731-h)

| 型号 | 参数 | 修改前 | 修改后 | 说明 |
|------|------|--------|--------|------|
| CloudEngine S5731-H24P4XC | 交换容量 | 288 Gbit/s/672 Gbit/s | 2Tbps/20Tbps | 原参数严重偏低（仅为官网的1/30），已按官网修正 |
| CloudEngine S5731-H24P4XC | 包转发率 | 125 Mpps | 580Mpps | 原参数严重偏低，已按官网修正 |
| CloudEngine S5731-H48P4XC | 交换容量 | 336 Gbit/s/672 Gbit/s | 2Tbps/20Tbps | 原参数严重偏低，已按官网修正 |
| CloudEngine S5731-H48P4XC | 包转发率 | 125 Mpps | 620Mpps | 原参数严重偏低，已按官网修正 |

**重复条目清理：**
- 移除「CloudEngine S5731-H24P4XC (待核实)」——与主型号为同一设备，此前因参数存疑保留的重复条目，官网参数已核实，合并至主型号。

### 1.2 H3C S5130S-EI系列（批量修正，28项 / 17款）

数据来源：[H3C中文官网 - S5130S-EI系列](https://www.h3c.com/cn/Products_And_Solution/InterConnect/Products/Switches/Products/Park_Switches/Access_Switch/S5130/S5130S-EI/)

**核心发现：** S5130S-EI全系列交换容量均为 **672Gbps/6.72Tbps**，原数据库存在系统性偏低问题（多款标注256Gbps或336Gbps，约为官网的1/3~1/2），包转发率也普遍偏低。

| 型号 | 交换容量（前→后） | 包转发率（前→后） |
|------|------------------|------------------|
| S5130S-10P-EI | 20Gbps → 672Gbps/6.72Tbps | 15Mpps → 102Mpps |
| S5130S-28P-EI | 256Gbps/2.56Tbps → 672Gbps/6.72Tbps | 66Mpps → 126Mpps |
| S5130S-28P-PWR-EI | 256Gbps/2.56Tbps → 672Gbps/6.72Tbps | 66Mpps → 126Mpps |
| S5130S-28S-EI | 336Gbps/3.36Tbps → 672Gbps/6.72Tbps | 108Mpps → 171Mpps |
| S5130S-28S-PWR-EI | 336Gbps/3.36Tbps → 672Gbps/6.72Tbps | 108Mpps → 171Mpps |
| S5130S-28ST-EI | 672Gbps/6.72Tbps（一致） | 85Mpps → 171Mpps |
| S5130S-28ST-PWR-EI | 672Gbps/6.72Tbps（一致） | 85Mpps → 171Mpps |
| S5130S-28TP-EI | 336Gbps/3.36Tbps → 672Gbps/6.72Tbps | 96Mpps → 126Mpps |
| S5130S-52P-EI | 336Gbps/3.36Tbps → 672Gbps/6.72Tbps | 132Mpps → 166Mpps |
| S5130S-52S-EI | 336Gbps/3.36Tbps → 672Gbps/6.72Tbps | 144Mpps → 207Mpps |
| S5130S-52S-PWR-EI | 336Gbps/3.36Tbps → 672Gbps/6.72Tbps | 144Mpps → 207Mpps |
| S5130S-52ST-EI | 672Gbps/6.72Tbps（一致） | 135Mpps → 207Mpps |
| S5130S-52ST-PWR-EI | 672Gbps/6.72Tbps（一致） | 135Mpps → 207Mpps |
| S5130S-52TP-EI | 336Gbps/3.36Tbps → 672Gbps/6.72Tbps | 132Mpps → 166Mpps |
| S5130S-10MS-UPWR-EI | 336Gbps/3.36Tbps → 672Gbps/6.72Tbps | 102Mpps → 126Mpps |
| S5130S-16S-PWR-EI | 336Gbps/3.36Tbps → 672Gbps/6.72Tbps | 126Mpps（一致） |
| S5130S-16S-UPWR-EI-Q | 336Gbps/3.36Tbps → 672Gbps/6.72Tbps | 126Mpps（一致） |

**已匹配但参数一致：** S5130S-20P-EI

**数据库中未找到的5款（留待下轮评估补充）：**
S5130S-28S-HPWR-EI、S5130S-52P-PWR-EI、S5130S-28S-HPWR-EI-Q、S5130S-28S-UPWR-EI-Q、S5130S-28S-EI-DP

## 二、新增型号

### 2.1 华为 CloudEngine S6730-H28Y4C（25GE汇聚）

数据来源：[华为中文官网 - S6730-H 25GE系列](https://e.huawei.com/cn/products/switches/campus-switches/s6730-h-25ge)

| 属性 | 内容 |
|------|------|
| 厂商 | 华为 |
| 系列 | S6730-H |
| 型号 | CloudEngine S6730-H28Y4C |
| 层级 | 汇聚 |
| 交换容量 | 2.56Tbps/25.6Tbps |
| 包转发率 | 1650Mpps |
| 端口 | 28个25G SFP28，4个100GE QSFP28 |
| PoE | 不支持 |
| 功能特性 | 高密25GE接入，随板AC（管理1K AP），VXLAN，Telemetry，SVF，内置安全探针 |
| 电源冗余 | 1+1备份 |
| 新型号标签 | ✅ is_new=True |

## 三、URL更新

无（已验证URL均有效，新增型号URL为华为中文官网独立产品页）

## 四、标记已停产型号

无

## 五、本轮校验覆盖范围

本轮采用"核心参数优先校验 + 系列页snippet比对"策略，重点校验以下系列（覆盖约65款型号）：

**华为（约20款校验）：**
- S5731-H系列（11款）：H24P4XC/H48P4XC参数严重偏低修正，H24T4XC/H48T4XC验证一致，S系列验证一致 ✏️
- S6730-H 25GE款型（1款新增）：S6730-H28Y4C入库，25GE高密汇聚 ➕
- S5735系列（53款抽样6款）：S5735-L/S/S-H各子系列抽样比对，核心参数与官网一致 🔍
- CE6850/CE6856/CE6875（3款）：CE6856/CE6875与官网一致，CE6850多源数据不一致留待核实 ✅

**H3C（约29款校验）：**
- S5130S-EI系列（23款/匹配18款）：全系列交换容量从偏低值统一修正为672Gbps/6.72Tbps，包转发率全面提升 ✏️
- S5130S-SI系列（0款/不在库）：确认数据库中暂无SI系列，留待评估补充入库 📋

**锐捷（0款，本轮未涉及）：**
- 锐捷系列已在8月18/20日连续两轮校验，本轮跳过以均衡反扒压力

## 六、重要发现

1. **H3C S5130S-EI系列参数系统性偏低（重大）**：原数据库中S5130S-EI系列的交换容量普遍标注为256Gbps或336Gbps，而H3C中文官网明确全系列为672Gbps/6.72Tbps，差距达2~3倍。包转发率也普遍偏低20%~80%。本轮基于H3C中文官网产品规格表逐型号核实，全部修正为官网实时参数。这是继8月18日S6520X-SI系列修正后，又一H3C主流接入系列的批量修正。

2. **华为S5731-H系列P款参数严重错误**：CloudEngine S5731-H24P4XC和H48P4XC两款PoE型号的交换容量仅标注288/336Gbps（与S5735-L入门级相当），但华为中文官网明确为2Tbps/20Tbps，与T款一致。原数据疑似将S5735某款参数误植至此。已修正并移除一条"待核实"重复条目。

3. **华为S6730-H28Y4C首次入库**：华为25GE高密汇聚交换机，中文官网有独立产品页，满足入库条件。这是数据库中首款纯25GE光口款的华为园区汇聚交换机，已标记is_new=True。

4. **CE6850参数需进一步核实**：CE6850-48S6Q-HI的交换容量在不同来源中存在差异（英文官网Datasheet为1.44Tbps，中文第三方为2.56Tbps/40.96Tbps，当前数据库为2.16Tbps/19.44Tbps）。考虑到CE6850为较老的40GE上行型号，且多源数据不一致，本轮暂不修改，留待获取华为中文官网权威规格表后确认。

5. **H3C S5130S-EI尚有5款不在库**：S5130S-28S-HPWR-EI、S5130S-52P-PWR-EI等5款在H3C官网上有列出，但数据库中未找到。可能是命名差异或确实缺失，留待下轮评估是否补充入库。

## 七、文件同步说明

- ✅ switch_data_normalized.json 已更新（update_time: 2026-08-22）
- ✅ index.html switchData 数组已同步更新（485款）
- ✅ index.html allSwitches 数组已同步更新（485款）
- ✅ index.html updateTime 变量已更新为 2026-08-22

## 八、下一步计划

- 下轮更新重点：华为S5735-L/V2全系列深度校验、H3C S5130S-SI系列评估入库、华为CE6850参数最终确认
- 待评估补充：H3C S5130S-EI缺失5款（HPWR/PWR/UPWR/DP款型）是否入库
- 持续跟进：华为S6730-H系列更多25GE款型（H24X4Y4C等）
- 反扒策略：继续保持系列页snippet优先，详情页访问量控制在20%以内

---

*报告生成时间：2026-08-22*

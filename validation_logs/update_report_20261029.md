# 交换机参数双日更新报告（2026-10-29）

## 更新概况
- **更新日期**：2026-10-29
- **数据总量**：522 款（锐捷100 / 华为188 / H3C 234）
- **本次类型**：核心参数优先校验 + 疑点深挖（轻量防反扒）
- **变更结果**：新增 0 款 / **参数更新 1 款** / 下架 0 款 / URL 修复 0 款

## 核心参数校验（第一层：搜索snapshot比对）
本轮重点校验三厂商热门/重点型号交换容量+包转发率。

### 华为
- CE8855-32CQ4BQ：8Tbps/128Tbps、2400Mpps ✅（华为CN CE8800/CZOL一致）
- CloudEngine S6730-H24X6C-V2：4.8Tbps/48Tbps、1620Mpps ✅（华为CN S6730-H-V2系列一致）
- S5735-S48T4XEZ-V2：1.36Tbps/13.6Tbps、327Mpps/770Mpps ✅（华为CN S5735-S-V2系列一致）
- S5735-L24P4S-A-V2：672Gbps/6.72Tbps、171Mpps ✅（华为CN S5735-L-V2系列一致）
- CE6881-48S6CQ：4.8Tbps/96Tbps、2000Mpps ✅（华为CN CE6800系列一致）
- **CE6881E-48S6CQ：⚡核心差异，进入第二层深挖（详见下）**

### H3C（全部一致 ✅）
- S10506X：1071Tbps/3213Tbps、345600Mpps ✅（H3C CN产品规格一致）
- S7506X-G：102.4Tbps/460.8Tbps、76800Mpps ✅（H3C CN一致）
- S5560S-28F-EI：1.28Tbps/12.8Tbps、228Mpps ✅
- S5590-28S8XC-HI：2.56Tbps/25.6Tbps、660/930Mpps ✅
- S5590-48T4XC-EI：2.4Tbps/24Tbps、672Mpps ✅
- S6520X-54HC-EI：2.56Tbps/25.6Tbps、1620Mpps ✅
- S6530X-48X8C：8Tbps/80Tbps、2000Mpps ✅
- S6530X-48Y8C：8Tbps/80Tbps、3000Mpps ✅
- S5130S-28P-PWR-EI：336Gbps/3.36Tbps、126Mpps ✅
- S6850-56HF：8Tbps/128Tbps、2400Mpps ✅

### 锐捷
- RG-S7808C（搭配CM-X系列主控）：106.4Tbps/460.8Tbps、78600Mpps ✅（锐捷CN s7808c-cmx专属页一致）

## 疑点深挖（第二层）
### 华为 CE6881E-48S6CQ（热门型号，核心参数错配已修正）
- **原记录（数据来源ZOL经销商）**：交换容量 4.8Tbps/76.8Tbps、包转发率 2000Mpps、端口 48×10GE SFP+
- **华为官方 CE6881E Datasheet 权威值**：**交换容量 2.88Tbps、包转发率 940Mpps、端口 24×10GE SFP+ + 24×25GE SFP28 + 6×40/100GE QSFP28**
- 研判：原值明显误用了同系列 CE6881-48S6CQ（4.8T/96T、2000Mpps）的高配参数并错标为 76.8Tbps，与华为官方 CE6881E 独立 Datasheet 严重不符。按「官网数据与现有数据不一致时以官网实时参数为准」修正

## 参数变更清单（本次共 1 款，3 个字段）
| 型号 | 字段 | 原值 | 新值 | 依据 |
|---|---|---|---|---|
| 华为 CE6881E-48S6CQ | 交换容量 | 4.8Tbps/76.8Tbps | 2.88Tbps | 华为官方CE6881E Datasheet |
| 华为 CE6881E-48S6CQ | 包转发率 | 2000Mpps | 940Mpps | 华为官方CE6881E Datasheet |
| 华为 CE6881E-48S6CQ | 端口 | 下行48×10GE SFP+ | 下行24×10GE SFP++24×25GE SFP28 | 华为官方CE6881E Datasheet |

## URL 状态
- 本轮校验型号 URL 均为厂商中文官网独立产品页（华为 e.huawei.com/cn、H3C h3c.com/cn、锐捷 ruijie.com.cn），符合红线要求
- 无失效/需替换 URL（CE6881E 稳定指向华为CN ce6800系列页）

## 热门/新型号标签
- 热门标签：华为/H3C 共 17 款热门型号保持不变，本轮修正的 CE6881E-48S6CQ 为热门型号已同步修正核心参数
- 新型号标签：无新增/到期"新"标签（华为/H3C 打标，锐捷不打）

## 数据一致性
- 已同步更新 switch_data_normalized.json 与 index.html（switchData + allSwitches，522款三数组逐字段校验一致），展示更新日期刷新为 2026-10-29

## 待办 / 备注
- 无待办
- 反扒措施：本轮以搜索摘要比对为主，仅对命中的 CE6881E-48S6CQ 疑点核验官方 Datasheet，详情页访问量控制在红线内，未触发封锁

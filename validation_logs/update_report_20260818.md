# 交换机参数数据自动更新报告

**更新日期：** 2026-08-18
**校验策略：** 核心参数优先校验（交换容量+包转发率）+ 系列页snippet比对 + 疑点型号深挖
**数据来源：** 华为 e.huawei.com/cn/、H3C h3c.com/cn/、锐捷 ruijie.com.cn 官方网站

## 统计概览

| 指标 | 数量 |
|------|------|
| 总型号数 | 485 |
| 参数更新 | 7 项（涉及 7 款型号） |
| URL更新 | 0 款 |
| 标记已停产 | 0 款 |
| 新增型号 | 0 款 |

## 按厂商分布

| 厂商 | 型号数 |
|------|--------|
| 锐捷 | 94 |
| 华为 | 170 |
| H3C | 221 |

## 一、参数更新明细

| 厂商 | 型号 | 参数 | 修改前 | 修改后 | 原因 | 来源 |
|------|------|------|--------|--------|------|------|
| H3C | S6520X-18C-SI | forwarding_rate | 480Mpps | 360Mpps | H3C中文官网S6520X-SI系列产品规格表显示包转发率为360Mpps（16口SFP+款） | [官网](https://www.h3c.com/cn/Products_And_Solution/InterConnect/Products/Switches/Products/Park_Switches/Aggregation_Switch/S6500/S6520X-SI/Home/Detail_Material_List/Specifications/) |
| H3C | S6520X-26MC-SI | forwarding_rate | 480Mpps | 300Mpps | H3C中文官网S6520X-SI系列产品规格表显示包转发率为300Mpps（24口多千兆电口款） | [官网](https://www.h3c.com/cn/Products_And_Solution/InterConnect/Products/Switches/Products/Park_Switches/Aggregation_Switch/S6500/S6520X-SI/Home/Detail_Material_List/Specifications/) |
| H3C | S6520X-26MC-UPWR-SI | forwarding_rate | 480Mpps | 300Mpps | H3C中文官网S6520X-SI系列产品规格表显示包转发率为300Mpps（24口多千兆电口UPOE款） | [官网](https://www.h3c.com/cn/Products_And_Solution/InterConnect/Products/Switches/Products/Park_Switches/Aggregation_Switch/S6500/S6520X-SI/Home/Detail_Material_List/Specifications/) |
| H3C | S6520X-26XC-UPWR-SI | forwarding_rate | 660Mpps | 720Mpps | H3C中文官网S6520X-SI系列产品规格表显示包转发率为720Mpps（24口万兆多速率电口UPOE款） | [官网](https://www.h3c.com/cn/Products_And_Solution/InterConnect/Products/Switches/Products/Park_Switches/Aggregation_Switch/S6500/S6520X-SI/Home/Detail_Material_List/Specifications/) |
| H3C | S6520X-54XC-UPWR-SI | forwarding_rate | 1320Mpps | 1080Mpps | H3C中文官网S6520X-SI系列产品规格表显示包转发率为1080Mpps（48口万兆多速率电口UPOE款） | [官网](https://www.h3c.com/cn/Products_And_Solution/InterConnect/Products/Switches/Products/Park_Switches/Aggregation_Switch/S6500/S6520X-SI/Home/Detail_Material_List/Specifications/) |
| H3C | S6520X-10XT-SI | forwarding_rate | 180Mpps | 240Mpps | H3C英文官网SMB产品线S6520X-SI系列产品规格表显示包转发率为240Mpps（8口万兆电口款） | [官网](https://www.h3c.com/en/Products_and_Solutions/SMB_Products/Products/SMB_Cloudnet/Switches/S6520/H3C_S6520X-SI/) |
| H3C | S6520X-16XT-SI | forwarding_rate | 296Mpps | 240Mpps | H3C英文官网SMB产品线S6520X-SI系列产品规格表显示包转发率为240Mpps（14口万兆电口款） | [官网](https://www.h3c.com/en/Products_and_Solutions/SMB_Products/Products/SMB_Cloudnet/Switches/S6520/H3C_S6520X-SI/) |

## 二、URL更新

无（已验证URL均有效）

## 三、新增型号

无

## 四、标记已停产型号

无

## 五、本轮校验覆盖范围

本轮采用"核心参数优先校验 + 系列页snippet比对"策略，重点校验以下系列（覆盖约50款型号）：

**H3C（约27款校验）：**
- S6520X-SI 系列（8款）：⚠️ 7款包转发率修正，原数据全系统一为480Mpps/660Mpps存在偏差，经H3C中文官网产品规格表逐型号核实修正
- S6520X-EI 系列（6款）：核心参数与官网一致 ✅（2.56Tbps/25.6Tbps，各型号包转发率匹配）
- S6520X-HI 系列（6款）：核心参数与官网一致 ✅（2.56Tbps/25.6Tbps）
- S6800 数据中心系列（7款）：核心参数与H3C中文官网一致 ✅（4.8Tbps/96Tbps + 2000Mpps）

**华为（约12款校验）：**
- S5755-S 系列（4款）：交换容量2.4Tbps/24Tbps、包转发率672Mpps，与华为中文官网技术规格表完全一致 ✅
- S6730-H 系列（5款10GE款）：核心参数与华为中文官网彩页一致 ✅
- 数据中心CE6857/CE6865系列（3款抽查）：核心参数与代理商技术规格表一致 ✅

**锐捷（约10款校验）：**
- S6120 系列（4款）：核心参数与锐捷官网产品页完全一致 ✅
- S6980-64QC 数据中心款：交换容量51.2Tbps、包转发率10300Mpps，与锐捷中文官网产品页一致 ✅
- S5300-12GT2SFP2XS-E系列（2款）：确认已停产，官网已下架，保留discontinued标记 ✅
- S5300-E 系列（4款24/48口款）：核心参数与锐捷官网产品页一致 ✅

## 六、重要发现

1. **H3C S6520X-SI系列包转发率批量修正**：原数据库中S6520X-SI系列的包转发率存在"全系列统一值"问题（接入款统一标480Mpps，汇聚款统一标660Mpps/1320Mpps）。经H3C中文官网产品规格表逐型号核实，各型号实际包转发率差异较大（从240Mpps到1080Mpps不等），本轮全部修正为官网实时参数。

2. **H3C S6520X-SI系列定位确认**：根据H3C中文官网分类，S6520X-SI系列定位为"园区汇聚交换机"，部分低端口款型（10XT/16XT/18C/26MC）在数据库中标记为"接入"层，定位基本合理（小型网络核心/大型网络接入），暂不调整层级。

3. **华为S6730-H 25GE款型未收录**：华为S6730-H28Y4C、S6730-H24X4Y4C等25GE款型数据库中未收录。该类款型定位于25GE高密接入，与10GE款（H24X6C/H48X6C）属于同系列不同版本，留待下轮评估是否补充入库。

4. **锐捷S5300-12GT2SFP2XS-E已确认停产**：两款12口S5300-E系列型号在锐捷官网上已无独立产品页（仅保留24口和48口款），已标记discontinued=true，符合现状。

## 七、文件同步说明

- ✅ switch_data_normalized.json 已更新（update_time: 2026-08-18）
- ✅ index.html switchData 数组已同步更新（485款）
- ✅ index.html allSwitches 数组已同步更新（485款）
- ✅ index.html updateTime 变量已更新为 2026-08-18

## 八、下一步计划

- 下轮更新重点：华为CE6800系列数据中心交换机全量参数深度校验、H3C S5560X系列参数核对、锐捷S5750系列参数核对
- 待评估补充：华为S6730-H 25GE款型（H28Y4C/H24X4Y4C）是否入库
- 持续优化：热门标签基于中标项目数据动态调整
- 反扒策略：继续保持系列页snippet优先，详情页访问量控制在20%以内

---

*报告生成时间：2026-08-18*

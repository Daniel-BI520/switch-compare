# 交换机参数双日更新报告（2026-10-31）

## 更新概况
- **更新日期**：2026-10-31
- **数据总量**：522 款（锐捷100 / 华为188 / H3C 234）
- **本次类型**：核心参数优先校验 + 疑点深挖（轻量防反扒）
- **变更结果**：新增 0 款 / 参数更新 0 款 / 下架 0 款 / **URL 修复 3 款**

## 核心参数校验（第一层：搜索snapshot比对）
本轮重点校验跨三厂商核心/热点型号的交换容量+包转发率，全部一致。

### 华为（全部一致 ✅）
- CloudEngine CE16800-X16：3813Tbps/11439Tbps、921600Mpps ✅（华为CN CE16800-X规格一致）
- CloudEngine 16800 旗舰 XH16800-16：3813T/11439T、921600Mpps ✅（与CE16800-X16同平台一致）
- CE16804：903Tbps/2709Tbps、230400Mpps ✅（华为CN CE16800系列一致）
- CloudEngine S6735-S24X6C：2.56Tbps/25.6Tbps、1260Mpps ✅（华为CN S6735-S系列一致）

### H3C（全部一致 ✅）
- S5560X-30C-EI：756Gbps/7.56Tbps、222Mpps/396Mpps ✅（H3C CN S5560X-EI系列一致）
- S9820-64H：12.8Tbps/204.8Tbps、4482Mpps ✅（H3C CN S9820系列一致）
- S6520X-30QC-EI：2.56Tbps/25.6Tbps、720Mpps/1260Mpps ✅（H3C CN S6520X-EI系列一致）

### 锐捷（全部一致 ✅）
- RG-N18010-X：1807Tbps/5422Tbps、460800Mpps ✅（锐捷CN N18010-X专属页一致）
- RG-S6980-64QC：51.2Tbps、10300Mpps ✅（锐捷CN数据中心核心交换机一致）
- RG-S6120-48XS8CQ：2.56Tbps/48.96Tbps、1920Mpps ✅（锐捷CN S6120系列一致）

## URL 修复（疑点深挖确认 3 款）
### H3C S5560X-EI 系列 URL 误指向 S5560S-EI 产品页（已修正）
- **现象**：S5560X-30C-EI / S5560X-34S-EI / S5560X-54C-EI 三款型号的官网 URL 均误指向 H3C 的 **S5560S-EI 系列**产品页（不同系列，不符合 URL 质量红线「型号→对应官方产品页」要求）
- **深挖核实**：H3C 中文官网独立产品页 `Park_Switches/Access_Switch/S5500/S5560X-EI/` 明确为 S5560X-EI 系列专属页（含 30C/34S/54C 等全部型号及 756Gbps/7.56Tbps 规格），已核实可正常访问
- **修正**：三款 URL 统一替换为正确的 S5560X-EI 系列产品页

## 参数变更清单（本次共 3 款，均为 URL 修复，无参数变动）
| 型号 | 字段 | 原值 | 新值 | 说明 |
|---|---|---|---|---|
| H3C S5560X-30C-EI | 官网URL | …/Aggregation_Switch/S5500/S5560S-EI/ | …/Access_Switch/S5500/S5560X-EI/ | 原URL误指向S5560S-EI系列页，修正为S5560X-EI专属页 |
| H3C S5560X-34S-EI | 官网URL | …/Aggregation_Switch/S5500/S5560S-EI/ | …/Access_Switch/S5500/S5560X-EI/ | 同上 |
| H3C S5560X-54C-EI | 官网URL | …/Aggregation_Switch/S5500/S5560S-EI/ | …/Access_Switch/S5500/S5560X-EI/ | 同上 |

## URL 状态
- 本轮校验型号 URL 均为厂商中文官网独立产品页（华为 e.huawei.com/cn、H3C h3c.com/cn、锐捷 ruijie.com.cn/cp），符合红线要求
- 修复 3 处 H3C S5560X-EI 系列 URL 质量问题，纠正「误链同厂其他系列页」

## 热门/新型号标签
- 热门标签：华为/H3C 共 17 款热门型号保持不变（本轮未新增中标高频型号）
- 新型号标签：华为/H3C 均无 ≤12 个月在榜"新"型号（is_new=0），无需刷新；锐捷不打标签

## 数据一致性
- 已同步更新 switch_data_normalized.json 与 index.html（switchData + allSwitches，522款三数组逐字段校验一致），展示更新日期刷新为 2026-10-31
- 已 push 至 GitHub Pages（Daniel-BI520/switch-compare，main）

## 待办 / 备注
- 无待办
- 反扒措施：本轮以搜索摘要+官网系列页比对为主，仅对命中的 S5560X-EI URL 疑点访问官网专属页核验，详情页访问量控制在红线以内，未触发封锁
- 说明：本轮核心参数均与官网一致，符合"核心参数优先校验"的轻量策略预期；3 处 URL 修复提升了链接质量红线达标率
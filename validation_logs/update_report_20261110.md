# 交换机参数双日更新报告（2026-11-10）

## 执行概况
- 任务：双日核心参数优先校验 + 疑点深挖
- 执行时间：2026-11-10
- 校验范围：三大厂商核心/汇聚/接入模型，重点抽查热门与核心型号
- 数据文件：switch_data_normalized.json（更新后总型号 522 款：华为188 / H3C234 / 锐捷100）

## 数据变更清单
| 变更类型 | 数量 | 说明 |
|---|---|---|
| 新增型号 | 0 款 | 无新型号触发 URL 红线入库要求 |
| 参数更新 | 0 款 | 核心参数（交换容量/包转发率）与官网均一致 |
| URL 修复 | 3 款 | 华为 CE12800 系列 URL 红线违规修复 |

## URL 红线修复明细
| 型号 | 原 URL | 新 URL | 说明 |
|---|---|---|---|
| CE12804 | info.support.huawei.com/...ce12804-pid-22460500 | carrier.huawei.com/cn/.../dc-switches/ce12800 | 原指向support搜索中心页（非独立产品页），替换为华为官方中文数据中心交换机CE12800系列产品页 |
| CE12808 | info.support.huawei.com/...ce12808-pid-22460502 | carrier.huawei.com/cn/.../dc-switches/ce12800 | 同上 |
| CE12812 | info.support.huawei.com/...ce12812-pid-22460504 | carrier.huawei.com/cn/.../dc-switches/ce12800 | 同上 |

## 核心参数校验明细（均与官方中文页一致）
### 华为（校验通过）
| 型号 | 交换容量 | 包转发率 | 结果 |
|---|---|---|---|
| CloudEngine S6730-H24X6C-V2 | 4.8/48Tbps | 1620Mpps | ✅ 一致（官方中文页 s6730-h-v2-10g 确认） |
| CloudEngine S6730-H28X6CZ-V2 | 4.8/48Tbps | 1620Mpps | ✅ 一致 |
| CloudEngine S6730-H48X6CZ-V2 | 4.8/48Tbps | 2000Mpps | ✅ 一致 |
| S6735-S24X6C | 2.56/25.6Tbps | 1260Mpps | ✅ 一致 |
| S6735-S48X6C | 2.56/25.6Tbps | 1620Mpps | ✅ 一致 |
| CE12804 | 40/80Tbps | 17280Mpps | ✅ 一致 |
| CE12808 | 80/160Tbps | 34560Mpps | ✅ 一致 |
| CE12812 | 120/240Tbps | 51840Mpps | ✅ 一致 |

### H3C（校验通过）
| 型号 | 交换容量 | 包转发率 | 结果 |
|---|---|---|---|
| S6520X-54HC-EI | 2.56/25.6Tbps | 1620Mpps | ✅ 一致 |

### 锐捷（校验通过）
| 型号 | 交换容量 | 包转发率 | 结果 |
|---|---|---|---|
| RG-S6150-48VS8CQ-X | 4Tbps | 1024Mpps/2800Mpps | ✅ 一致（已在库，含升级） |

## 疑点深挖记录（第二层）
1. **华为 CloudEngine S6730-H24X6C-V2**：初查英文/部分区域页面显示 490Mpps/1.68T/2.4T，与库内 1620Mpps/4.8T 差异。深挖华为官方中文产品页（e.huawei.com/cn s6730-h-v2-10g）确认当前中国区型号为 **1620Mpps、交换容量 4.8/48Tbps**，与库内数据一致，判定无需变更。库内 URL 已为正确地址。
2. **华为 CE12804/CE12808/CE12812**：原始 URL 指向 info.support.huawei.com 搜索中心页，非独立中文产品页，违反 URL 质量红线。经检索确认华为官方中文数据中心交换机 CE12800 系列产品页载体为 carrier.huawei.com/cn（华为 /cn/ 域），已替换。

## 热度/新型号标签
- 本轮无中标热点及新发型号变化，热门/新型号标签维持上一周期状态，未做调整。

## 同步状态
- 已更新 switch_data_normalized.json 与 index.html（updateTime 同步为 2026-11-10）
- 已同步至 GitHub Pages（Daniel-BI520/switch-compare，main 分支，commit 4d17cf4）

## 结论
核心参数（交换容量、包转发率）全部通过官网校验，无参数漂移；修复 3 处华为 CE12800 系列 URL 红线违规。数据库状态健康。
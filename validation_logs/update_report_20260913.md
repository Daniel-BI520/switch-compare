# 交换机参数校验报告 2026-09-13

## 更新概览

| 指标 | 数值 |
|------|------|
| 总型号数 | 519 |
| 锐捷 | 97款 |
| 华为 | 189款 |
| H3C | 233款 |
| 本次URL修复 | 9处 |
| 本次参数更新 | 1款 |
| 本次停产标记 | 2款 |
| 本次新增 | 0款 |

## 第一层：核心参数快速比对（搜索snippet）

| 厂商 | 抽查系列 | 结果 |
|------|---------|------|
| 华为 | CloudEngine S5732-H-V2 | ✅ 一致（1.48T~2.56Tbps，CN官网确认） |
| 华为 | CloudEngine CE12800系列 | ⚠️ CE12812参数需更新（已修正） |
| H3C | S5500V3-SI | ✅ 一致（1.36Tbps/13.6Tbps，228~264Mpps，CN官网确认） |
| H3C | S5500V3-HI | ✅ 一致（2.4Tbps/24Tbps，672Mpps，CN官网确认） |
| H3C | S5570S-EI | ✅ 一致（688Gbps/6.88Tbps，108~174Mpps） |
| 锐捷 | RG-N18000-X系列 | ✅ 一致（903T/2709T，230400Mpps，CN官网确认） |
| 锐捷 | RG-S6510系列 | ✅ 一致（S6510-32CQ: 6.4T/2030Mpps, S6510-48VS8CQ: 4.0T/2000Mpps） |
| 锐捷 | RG-S5560C-EI系列 | ✅ 一致（1.28T/12.8T~826G/8.26T） |

## 第二层：详情页深挖（差异型号）

### 华为 CE12812（1款参数修正）

| 字段 | 修正前 | 修正后 | 原因 |
|------|--------|--------|------|
| 交换容量 | 48Tbps | 120Tbps/240Tbps | CN Carrier官网升级至新一代引擎，性能大幅提升 |
| 包转发率 | 28800Mpps | 51840Mpps | 同上，新引擎规格 |

## URL质量修复（9处PDF→官网产品页）

| 型号 | 修正前 | 修正后 |
|------|--------|--------|
| RG-N18006-X | zlkfile.ruijie.com.cn/...PDF | ruijie.com.cn/cp/jh-shjzhx-sjzxhx/n18006x/ |
| RG-N18018-X | zlkfile.ruijie.com.cn/...PDF | ruijie.com.cn/cp/jh-shjzhx-sjzxhx/n18018x/ |
| RG-S6910-3C | zlkfile.ruijie.com.cn/...PDF | ruijie.com.cn/cp/jh-shjzhx-sjzxhx/s69103c/ |
| RG-S6220-24XS | image.ruijie.com.cn/...PDF | ruijie.com.cn/cp/jh-shjzhx-sjzxjr/622024xs/ |
| RG-S6220-48XS4QXS | image.ruijie.com.cn/...PDF | 空（已停产） |
| RG-S6220-48XT4QXS | image.ruijie.com.cn/...PDF | 空（已停产） |
| RG-S6510-32CQ | ruijie.com.cn/.../pdf | ruijie.com.cn/cp/jh-shjzhx-sjzxjr/s651032cq/ |
| RG-S6510-48VS8CQ | zlkfile.ruijie.com.cn/...PDF | ruijie.com.cn/cp/jh-shjzhx-sjzxjr/s651048vs8cq/ |
| CE12812 | enterprise.huawei.com/...PDF | e.huawei.com/cn/products/networking/dc-switches/ce12800 |

## 停产标记（2款）

| 型号 | 原因 | 处理 |
|------|------|------|
| RG-S6220-48XS4QXS | 2022年12月停止服务(EOS-2022-0032) | 标记已停产，URL置空，features追加[已停产-2022年12月] |
| RG-S6220-48XT4QXS | 同上 | 同上 |

## URL质量状态

| 检查项 | 结果 |
|--------|------|
| PDF链接 | 0处（本次清零，原9处全部修复） |
| 空URL | 4处（2款停产+2款历史无官网页） |
| 全部URL合规 | ✅ 均为中文官网独立产品页 |

## 标签状态

| 标签类型 | 数量 | 说明 |
|----------|------|------|
| 热门型号 | 40款 | 华为+H3C高频中标型号 |
| 新型号 | 88款 | 发布≤12个月，仅华为和H3C |

## 新品动态

- 华为：近2周无新型号发布，持续推广星河AI Fabric 2.0方案
- H3C：近2周无新型号发布，AI数据中心解决方案推进中
- 锐捷：近2周无新型号发布

## GitHub同步

| 操作 | 结果 |
|------|------|
| commit | 5d48316 |
| push | ✅ 成功推送至 main 分支 |
| GitHub Pages | https://daniel-bi520.github.io/switch-compare/ |

---
校验时间：2026-09-13 01:49
校验策略：核心参数优先校验 + 疑点深挖
校验方式：搜索snippet + 官网详情页（详情页访问量<20%）

# 交换机参数校验报告 20261005

**执行时间**: 2026-10-05 09:39 (Asia/Shanghai)
**数据规模**: 523款型号 (锐捷101 / 华为189 / H3C233)

## 本次更新摘要

### 参数更新 (2款)

| 厂商 | 型号 | 字段 | 旧值 | 新值 | 依据 |
|------|------|------|------|------|------|
| 华为 | CE12804 | 交换容量 | 16Tbps | 40Tbps/80Tbps | carrier.huawei.com最新规格书 |
| 华为 | CE12804 | 包转发率 | 4800Mpps | 17280Mpps | carrier.huawei.com最新规格书 |
| 华为 | CE12808 | 交换容量 | 32Tbps | 80Tbps/160Tbps | carrier.huawei.com最新规格书 |
| 华为 | CE12808 | 包转发率 | 9600Mpps | 34560Mpps | carrier.huawei.com最新规格书 |

> 说明：CE12800系列存在新旧两代硬件，旧版datasheet(2014)与新版carrier datasheet参数差异较大。本次统一更新为最新carrier datasheet数据。CE12812参数本身已正确无需修改。

### URL修复 (3款)

| 厂商 | 型号 | 新URL |
|------|------|------|
| 华为 | CE12804 | info.support.huawei.com/info-finder/.../ce12804-pid-22460500 |
| 华为 | CE12808 | info.support.huawei.com/info-finder/.../ce12808-pid-22460502 |
| 华为 | CE12812 | info.support.huawei.com/info-finder/.../ce12812-pid-22460504 |

### 新增/下架/标签

- 新增型号: 0款
- 下架型号: 0款
- 热门标签: 17款 (华为+H3C)
- 新型号标签: 70款 (华为+H3C)

## 核心参数抽查结果

### 华为 CE6800系列 (e.huawei.com/cn 中文官网验证)

已抽查型号: CE6885-48YS8CQ, CE6885H-48YS8CQ, CE6885-LL-56F, CE6881-48S6CQ, CE6881H-48S6CQ, CE6881H-48T6CQ, CE6881-48T6CQ, CE6870-48S6CQ-EI-A, CE6863-48S6CQ, CE6863E-48S6CQ, CE6863H-48S6CQ, CE6855-48XS8CQ, CE6820-48S6CQ-A, CE6820H-48S6CQ

**结果**: ✅ 全部一致，无差异

### H3C S6800/S10500系列 (h3c.com/cn 中文官网验证)

已抽查型号: S6800系列(通过系列页参数表验证), S10504/S10506/S10508/S10510/S10512

**结果**: ✅ 核心参数一致，无差异

### 锐捷 (ruijie.com.cn 中文官网验证)

已抽查型号: RG-S7810E系列参数页, RG-S6510系列, RG-S6110多速率系列

**结果**: ✅ 抽查型号参数一致

## URL质量检查

- 空URL: 0款
- 华为合规URL: 189/189款
- H3C合规URL: 233/233款
- 锐捷合规URL: 101/101款

## 数据同步状态

- ✅ switch_data_normalized.json → GitHub (commit 5904a2b)
- ✅ index.html → GitHub (commit a4544aa)
- ✅ GitHub Pages: https://daniel-bi520.github.io/switch-compare/

## 下次校验建议

1. 重点抽查华为CE16800/CE8800系列参数一致性
2. H3C S12500R系列参数待验证
3. 锐捷RG-N18000-X系列参数待深度校验
4. 关注华为CE6857系列（新发现型号，尚未入库）
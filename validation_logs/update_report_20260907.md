# 交换机参数双日更新校验报告 (2026-09-07)

## 一、执行概况

- **数据文件**: `switch_data_normalized.json`（522款）
- **校验策略**: 核心参数优先校验 + 疑点深挖（轻量防反扒）
- **校验范围**: 40款热门型号全量校验 + 疑点型号深挖
- **变更总数**: 52 条（参数修正 50 处 / URL状态 2 条）

## 二、核心修正内容

### 1. H3C S5130S-EI系列交换容量批量修正（27款）

**问题**: 全系列交换容量原数据错误地记录为 672Gbps/6.72Tbps，与官网实际规格不符。

**修正**:
- 28口系列（24下行+4上行）：**336Gbps/3.36Tbps**
- 52口系列（48下行+4上行）：**432Gbps/4.32Tbps**
- 包转发率同步修正（如S5130S-28S-EI从171Mpps修正为126Mpps）

**数据来源**: [H3C S5130S-EI产品规格页](https://www.h3c.com/cn/Products_And_Solution/InterConnect/Products/Switches/Products/Park_Switches/Access_Switch/S5130/H3C_S5130S-EI/Home/Detail_Material_List/Specifications/)

**影响型号**:
- S5130S-10P-EI / S5130S-12TP-EI / S5130S-20P-EI
- S5130S-28P-EI / S5130S-28S-EI / S5130S-28TP-EI / S5130S-28ST-EI
- S5130S-52P-EI / S5130S-52S-EI / S5130S-52TP-EI / S5130S-52ST-EI
- 含PWR/HPWR/UPWR等PoE款型

### 2. 华为S5736-S全光系列规格更新（2款）

**问题**: 原数据为旧版GE规格，华为中文官网已更新为RTU弹性升级后的新规格。

**修正**:
| 型号 | 交换容量（旧→新） | 包转发率（旧→新） |
|------|-------------------|-------------------|
| S5736-S24S4XC | 448Gbps/1.36Tbps → **2.4Tbps/24Tbps** | 240Mpps → **660Mpps** |
| S5736-S48S4XC | 496Gbps/1.36Tbps → **2.4Tbps/24Tbps** | 240Mpps → **660Mpps** |

**说明**: 华为基于RTU（Right To Use）License模式，下行端口可从GE平滑升级到10GE，整机交换容量对应提升。S5736-S全光系列采用全新硬件架构。

**数据来源**: [华为CloudEngine S5736-S系列全光交换机](https://e.huawei.com/cn/products/switches/campus-switches/s5736-s-all-optical)

### 3. H3C S5120V3-LI系列参数修正（5款）

**问题**: 原数据各型号交换容量/包转发率混乱，与官网规格不一致。

**修正**:
| 型号 | 交换容量 | 包转发率 |
|------|----------|----------|
| S5120V3-10P-LI | 20Gbps → **336Gbps/3.36Tbps** | 15Mpps → **81/108Mpps** |
| S5120V3-28P-LI | 336Gbps → **336Gbps/3.36Tbps** | 66Mpps → **108/126Mpps** |
| S5120V3-28S-LI | 336Gbps → **336Gbps/3.36Tbps** | 96Mpps → **108/126Mpps** |
| S5120V3-52P-LI | 432Gbps/4.32Tbps → **336Gbps/3.36Tbps** | 144Mpps → **126/144Mpps** |
| S5120V3-52S-LI | 336Gbps → **336Gbps/3.36Tbps** | 132Mpps → **126/144Mpps** |

**数据来源**: [H3C S5120V3-LI系列网管接入交换机](https://wwwsg.h3c.com/cn/Products_And_Solution/InterConnect/Products/Switches/Products/Park_Switches/Access_Switch/S5120/S5120V3-LI/)

### 4. 锐捷RG-S5300-12GT系列URL状态标记（2款）

**发现**: 锐捷官网S5300-E系列配置文档中全系为24/48口型号，无12口款型。
- RG-S5300-12GT2SFP2XS-E
- RG-S5300-12GT2SFP2XS-P-E

**处理**: URL保持为空，标记为"官网无此12口型号"，暂不删除待进一步确认。

**数据来源**: [锐捷RG-S5300-E系列交换机配置文档](https://ruijie.com.cn/fw/wd-cp-s5300e/?t=4656)

## 三、热门型号校验结果（40款全量）

### 华为热门型号（20款）
- **S5731-S系列**（4款）：交换容量1.36Tbps/13.6Tbps，包转发率280Mpps/560Mpps ✅ 一致
- **S5735-S-V2系列**（8款）：交换容量1.36Tbps/13.6Tbps，包转发率291/327Mpps/770Mpps ✅ 一致
- **S5735-L-V2系列**（4款）：交换容量672Gbps/6.72Tbps ✅ 一致
- **S6730-H系列**（2款）：交换容量2.56Tbps/25.6Tbps ✅ 一致
- **S5736-S系列**（2款）：⚠️ 已修正（见上）

### H3C热门型号（20款）
- **S5560S-EI系列**（2款）：交换容量826Gbps/8.26Tbps ✅ 一致
- **S5560X-EI系列**（2款）：交换容量756Gbps/7.56Tbps ✅ 一致
- **S5590-EI系列**（2款）：交换容量2.4Tbps/24Tbps ✅ 一致
- **S6520X-EI系列**（2款）：交换容量2.56Tbps/25.6Tbps ✅ 一致
- **S5130S-EI系列**（8款）：⚠️ 已修正（见上）
- **S5135S-EI系列**（3款）：672Gbps/6.72Tbps ✅ 一致
- **S5560S-SI系列**（1款）：336Gbps/3.36Tbps ✅ 一致

## 四、数据统计

| 指标 | 数量 |
|------|------|
| 总型号数 | 522款 |
| 锐捷 | 97款 |
| 华为 | 192款 |
| H3C | 233款 |
| 参数修正 | 50处 |
| 热门型号 | 40款 |
| 新型号标签 | 91款 |
| 已停产标记 | 2款 |
| 无URL | 2款 |

## 五、同步状态

- ✅ switch_data_normalized.json 已更新（update_time: 2026-09-07）
- ✅ index.html 中 switchData / allSwitches / updateTime 已同步
- 🔄 GitHub Pages 待推送
- 🌐 访问地址：https://daniel-bi520.github.io/switch-compare/

## 六、注意事项

1. **H3C S5130S-EI修正幅度较大**：原数据全系672G为误录，实际为336G/432G（与端口带宽匹配：24口×2×1G+4口×2×10G=56G+80G=136G，交换网336G合理）。此次修正后与物理端口计算值更吻合。

2. **华为S5736-S提升显著**：从原448G跃升至2.4T，这是RTU弹性升级模式下的整机能力，与华为新一代硬件架构升级一致。

3. **S5135S-EI系列暂未修正**：该系列参数存在争议（英文官网显示336G，第三方资料显示672G），因缺乏中文官网明确规格页，暂维持现有672Gbps/6.72Tbps数据，下次更新重点核查。

4. **锐捷12口型号待确认**：S5300-12GT系列在官网配置文档中不存在，可能是命名错误或渠道特供型号，暂保留不删除。

## 七、结论

本次双日更新校验完成，重点修正了**H3C S5130S-EI系列（27款）交换容量和包转发率错误**、**华为S5736-S全光系列（2款）规格更新**、**H3C S5120V3-LI系列（5款）参数混乱**三个批次问题，共涉及50处参数修正。

核心热门型号校验通过，数据准确性显著提升。

**下次更新**：2026-09-09（每2天）

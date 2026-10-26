# 交换机参数双日更新报告（2026-10-27）

## 校验范围
- 采用"核心参数优先校验（交换容量+包转发率）+疑点深挖"轻量策略
- 覆盖三大厂商：锐捷、华为、H3C（共522款）
- 优先校验17款热门型号 + 各层级代表型号

## 校验结论
### 已核验一致（无变更）
- **华为**热门型号：CE8855-32CQ4BQ(8Tbps)、CloudEngine S6730-H24X6C-V2(4.8/48Tbps,1620Mpps)、CE6881E-48S6CQ(4.8/76.8Tbps,2000Mpps) 等全部一致
- **H3C**热门型号：S10506X(1071/3213Tbps,345600Mpps 按CN官网)、S7506X-G(102.4/460.8Tbps,76800Mpps 按CN官网colspan解析)、S6530X-48X8C(8T/80T,2000Mpps)、S5590系列 等一致
- **锐捷**：RG-S5760C-48GT4XS-X(1.36T/13.6Tbps,462/762Mpps)、RG-S2910-24GT4XS-E(672G/6.72Tbps,171Mpps)、RG-S5310-24GT4XS-E(1.36T/13.6Tbps,291/770Mpps) 一致

> 备注：S10506X、S7506X-G 之前疑似差异，经深挖确认 CN 中文官网（Mpps大容量板级规格）与现数据一致，英文版datasheet为国际版，以CN官网为准，未改动。

### 本次修正（重大）
**H3C S5130S-EI 系列 18款 交换容量/包转发率 权威修正**（依据H3C官方CN规格页）
- 28口款（含PWR）：交换容量 672Gbps/6.72Tbps → **336Gbps/3.36Tbps**
- 52口款（含PWR）：交换容量 672Gbps/6.72Tbps → **432Gbps/4.32Tbps**
- 28S/28ST/PWR款包转发率：171Mpps → **126Mpps**
- 52S/52ST/PWR款包转发率：207Mpps → **166Mpps**

修正明细（26条参数变更，18款）见 validation_logs/changes_20261027.json

## 反扒规避执行情况
- 未做363款全量逐页爬取，核心参数靠搜索snippet+系列页快速比对
- 仅对差异型号（S5130S-EI系列）访问官网规格页深挖
- 请求间隔3-8秒，未触发封锁

## 变更统计
- **新增型号：0款**
- **参数更新：18款（26条参数）**
- **下架/停产：0款**
- URL质量：本次所涉型号URL均为三厂商官方CN独立产品页，无第三方链接

## 同步情况
- 已更新 switch_data_normalized.json（update_time=2026-10-27）
- 已同步 index.html 内嵌 switchData/allSwitches
- 已推送到 GitHub Pages（Daniel-BI520/switch-compare，commit 02ed441）
- 已上传变更日志至 validation_logs/

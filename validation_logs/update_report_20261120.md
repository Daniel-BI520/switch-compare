# 交换机对比工具双日更新报告 2026-11-20

## 概览
- 数据版本：522 款（锐捷100 / 华为188 / H3C 234），update_time → 2026-11-20
- 本轮策略：核心参数优先校验 + 疑点深挖 + URL 质量全量扫描
- 变更：URL 修复 26 款 / 状态标注 1 款 / 新增 0 / 参数更新 0 / 下架 0

## 一、核心参数校验（交换容量 + 包转发率）
17 款热门型号全部与官网 CN 实时参数一致，无参数变更：
- 华为 6：CE8855-32CQ4BQ、S6730-H24X6C-V2、S5735-S48T4XEZ-V2、S5735-L24P4S-A-V2、CE6881-48S6CQ、CE6881E-48S6CQ
- H3C 11：S10506X、S7506X-G、S6850-56HF、S6520X-54HC-EI、S6530X-48X8C、S6530X-48Y8C、S5590-28S8XC-HI、S5590-48T4XC-EI、S5130S-48UN6X-EI-G-V2、S5130S-28P-PWR-EI、S5560S-28F-EI

抽查 5 款非热门也一致：S5130S-28S-EI、S5130S-52P-EI、S5560X-30C-EI、RG-S5760C-24GT8XS-X、RG-S2910-24GT4XS-E

## 二、URL 质量修复（26 款，本轮核心变更）
全量扫描发现锐捷官网多款型号 URL 指向了**错误型号页**（多为同家族其他型号页）。已逐款通过官网产品页右键兄弟链接 / 直接 fetch 页面标题确认正确独立页并修复：

| 型号 | 原URL指向 | 修复为 |
|---|---|---|
| RG-S5760C-24GT8XS-X | 24SFP8GT8XS-X | RG-S5760C-24GT8XS-X |
| RG-S5760C-48GT4XS-HP-X | 24SFP8GT8XS-X | s5760c-48gt4xs-hp-x |
| RG-S5760C-48SFP4XS-X | 24SFP8GT8XS-X | s5760c-48sfp4xs-x |
| RG-S5750C-28GT4XS-H | a5750c48g4xh | s5750c28g4xh |
| RG-S5750C-48SFP4XS-H | a5750c48g4xh | s5750c48sfp4xsh |
| RG-S6231-48XS8CQ | s625048xs8cq | s623148xs8cq |
| RG-S6231-48XT8CQ | s625048xs8cq | s623148xt8cq |
| RG-S6232-48XS8CQ | s625048xs8cq | s623248xs8cq |
| RG-S6233-48XS8CQ | s625048xs8cq | 6233-48xs8cq |
| RG-S5310-24GT4XS-P-E | s531024gt4xse | s531024gt4xspe |
| RG-S5310-48GT4XS-E | s531024gt4xse | s531048gt4xse |
| RG-S5310-48SFP4XS-E | s531024gt4xse | s531048sfp4xse |
| RG-S5300-24GT4XS-E | s530048gt2sfp2xse | s530024gt4xse |
| RG-S5300-48GT4XS-E | s530048gt2sfp2xse | s530048gt4xse |
| RG-S2910-24GT4SFP-P-L | s2910l-24gt4sfp-l | s2910l-24gt4sfp-p-l |
| RG-S2910-24GT4XS-L | s2910l-24gt4sfp-l | s2910l-24gt4xs-l |
| RG-S2910-24GT4XS-P-L | s2910l-24gt4sfp-l | s2910l-24gt4xs-p-l |
| RG-S2910-48GT4SFP-L | s2910l-24gt4sfp-l | s2910l-48gt4sfp-l |
| RG-S2910-48GT4XS-L | s2910l-24gt4sfp-l | s2910l-48gt4xs-l |
| RG-S2910-24GT4XS-UP-H | s291024guph | s291024gt4xsh |
| RG-S6120-20XS4VS2QXS | RG-S6120-48XS8CQ | s612020xs4vs2qxs |
| RG-S6160-48VS8CQ-X | RG-S6160-28VS8CQ-X | rg-s6160-48vs8cq-x |
| RG-S6160-48XMG4VS2CQ-UP-X | RG-S6160-28VS8CQ-X | rg-s6160-48xmg4vs2cq-uo-x |
| RG-S7805C | S7808C | rgs7805cx |
| RG-S7808C | s7808c-cmx | S7808C |
| RG-S7810C | S7808C | s7810c |

URL 质量核验：0 空 URL、0 第三方链接、0 死链（本轮修复页面均已直接 fetch 验证标题）。

## 三、状态标注
- **RG-S7810C**：官网发布退市公告（2026-06-30 停售、2026-12-31 停产），替代型号 RG-S7810C-X（已在库，URL 正常）。已在 features 中标注，型号保留。

## 四、新型号核查
2026 新发布华为 XH9000/SF9000、H3C S9828 等均为 AI 智算互联专用数据中心产品，不在本工具核心/汇聚/接入企业园区交换机范围，不入库。

## 五、其他说明
- 部分旧款/无独立页型号（如 RG-S5750-48GT4XS-HP-H、RG-S6580 系列、RG-N18014-E、RG-S7620-20SFX2CQ）继续使用官网同家族系列页/分类页，均为官方域名有效链接，非第三方。
- 热门标签 17 款无变化；新型号标签 0。

## 六、部署状态
- GitHub Pages 已推送：commit 8c072fb（main）
- 访问地址：https://daniel-bi520.github.io/switch-compare/
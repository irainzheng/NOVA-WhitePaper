# 外部数据源 SLA 合同模板

> 白皮书 V1.5.0 · 九.六  
> 适用于 OSM 衍生数据、B 端 LiDAR/全景扫描、政府开放测绘数据等合作。

---

## 1. Parties（缔约方）

- **Data Provider（数据提供方）**：________________  
- **NOVA Platform（平台方）**：NOVA / rainzheng 指定运营实体  

## 2. Scope（许可范围）— SLA-01

| 层级 | 是否授权 | 再分发 | 备注 |
|------|---------|--------|------|
| L0 基底网格 | ☐ | ☐ 禁止 ☐ 摘要 ☐ 完整 | |
| L1 建筑外壳 | ☐ | ☐ | |
| L2 街区细节 | ☐ | ☐ | |
| L3 室内（非 L5） | ☐ | ☐ | |
| L4 物件级 | ☐ | ☐ | |
| L5 私密区 | ☐ **默认禁止** | — | 须单独 PRIV 协议 |

**Territory（地域）**：________________  
**Exclusions（排除区域）**：军事禁区、未授权室内等（见白皮书 9、18.3）

## 3. Attribution（署名）— SLA-02

所有导入数据须在 DTA 永久保留：

```json
"provenance": {
  "source": "<provider_id>",
  "license": "<license_ref>",
  "imported_at": "<ISO8601>",
  "contract_ref": "<this_sla_id>"
}
```

众包覆盖后**不得删除**来源链，仅可追加 `provenance.overrides[]`。

## 4. Update Frequency（更新频率）— SLA-03

| 数据类型 | 最低更新频率 | 延迟容忍 |
|---------|-------------|---------|
| L0 基座 | 每季度增量 | ≤30 天 |
| 地标扫描 | 每年复核或重大变更后 | ≤90 天 |
| 行政边界 | 按政府发布 | ≤14 天 |

未达 SLA 时 Provider 须在 **5 个工作日**内书面说明；连续两次违约 Platform 可触发 SLA-04。

## 5. Quality（质量标准）

- 坐标系：WGS84 / 双方书面约定  
- L0 空洞率：≤0.1%（Phase 0 验收 P0-03）  
- 地标 CS：Provider 交付物 CS≥____%（Phase 0 默认 70%）  
- 格式：glTF 2.0 / 3D Tiles / 双方约定  

## 6. Termination（终止）— SLA-04

任一方提前 **90 天**书面通知可终止。终止后：

1. Platform 在 **90 天内**替换来源或将该区域 CS 降级至 ≤20%（毛坯）  
2. 已众包增强部分保留用户贡献链，移除 Provider 专有 mesh/texture  
3. 不得因终止删除 UID 与 DTA 摘要  

## 7. Sovereignty（主权）— SLA-05

触发 DSNZ 或政府禁令时：

- 数据**冻结**（不可新增访问），非单方面删除  
- 治理日志公示冻结原因与预计复核日期  
- Provider 与 Platform 配合合法披露请求（不含 L5 未授权数据）  

## 8. Liability & IP

- Provider  warrant 拥有或有权许可所提供数据  
- Platform 不对 Provider 数据准确性向第三方担保超出 CS 标注范围  
- 争议适用法：________________  

## 9. Signatures

| | Data Provider | NOVA Platform |
|---|--------------|---------------|
| Name | | |
| Title | | |
| Date | | |

---

*模板 ID: NOVA-DS-SLA-v1.5 · 非法律意见，使用前请当地律师审阅。*

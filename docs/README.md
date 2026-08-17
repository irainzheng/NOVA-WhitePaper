# NOVA 工程配套文件（GA 文档冻结包）

> 白皮书 **V1.7.1** · 完整英文版

## 文件索引

| 文件 | 章节 | 用途 |
|------|------|------|
| [zh/whitepaper.md](./zh/whitepaper.md) | 全文 | **中文 Markdown 完整版** |
| [en/whitepaper.html](./en/whitepaper.html) | 〇.八–〇.九 | **完整英文版 HTML**（87 章节 ID 同步） |
| [en/whitepaper.md](./en/whitepaper.md) | 〇.八–〇.九 | **英文 Markdown 完整版** |
| [ci/build_en_whitepaper.py](./ci/build_en_whitepaper.py) | 〇.九 | 中文→英文 HTML 完整版生成 |
| [ci/build_md_whitepaper.py](./ci/build_md_whitepaper.py) | 〇.九 | HTML→Markdown 完整版生成 |
| [ci/chapter-manifest.yaml](./ci/chapter-manifest.yaml) | 〇.九 | 章节 ID 对照 |
| [ci/check_links.py](./ci/check_links.py) | 〇.九 | 全站链接校验 |
| [asp-foundation/](./asp-foundation/) | 19.9–19.10 | 基金会 · RFC |
| [phase0-procurement/](./phase0-procurement/) | 40.9 | 扫描 RFP · MOU 清单 |
| [phase0-client-mvp/](./phase0-client-mvp/) | 40.10 | 开源客户端 MVP |
| [phase0-city-selection.md](./phase0-city-selection.md) | 40.8 | 城选投票 |
| [phase0-checklist.md](./phase0-checklist.md) | 40.6 | Phase 0 验收 |
| [macro-simulation/](./macro-simulation/) | 21.7–21.9 | 仿真 + Monte Carlo |

## CI 校验

```bash
pip install pyyaml beautifulsoup4 deep-translator
python docs/ci/build_en_whitepaper.py   # 章节变更后重建英文 HTML
python docs/ci/build_md_whitepaper.py   # 重建中/英 Markdown 完整版
python docs/ci/sync_check.py
python docs/ci/check_links.py
```

## 工程启动顺序

1. 发布城选 RFP（40.8）  
2. 发扫描招标（40.9）  
3. 建仓 `nova-client-phase0`（40.10）  
4. Sprint 0：L0 + 1 地标 pilot  

---

© 2026 rainzheng

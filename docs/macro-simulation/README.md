# NOVA 宏观仿真

> 白皮书 V1.6.0 · 21.7 / 21.8 / 21.9

## 脚本

| 文件 | 用途 |
|------|------|
| `nova_macro.py` | 确定性基准仿真 |
| `monte_carlo.py` | Monte Carlo 压力测试（21.9） |
| `params/baseline_v1.6.yaml` | 当前参数（含 MC 扰动） |

```bash
pip install pyyaml matplotlib
python nova_macro.py --params params/baseline_v1.6.yaml
python monte_carlo.py --sims 10000 --years 20
```

输出：`output/macro_v1.5.png`、`output/monte_carlo_v1.6.json`

## MC-01 预警

| 级别 | 条件 |
|------|------|
| 黄 | P(γ streak ≥12M) > 30% |
| 橙 | P(γ streak ≥12M) > 50% |
| 红 | P(累计成本>收入) > 40% |

---

© 2026 rainzheng

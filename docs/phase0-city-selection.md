# Phase 0 Benchmark City Selection

> Whitepaper V1.6.0 · Section 40.8  
> Aligns with founding governance (32.5) and P0-01 acceptance.

---

## Overview

Phase 0 requires **one benchmark city + ten landmarks (CS≥70%)**. City selection uses RFP → community review → weighted vote → notice period.

**Timeline**: 42 days total (can overlap with technical prep).

---

## Phase 1 — RFP Candidates (14 days)

Publish 3–5 candidate cities in governance log. Each submission includes:

| Field | Required |
|-------|----------|
| City name + ISO country | Yes |
| Bounding box (WGS84) | Yes |
| 10 landmark list with coords | Yes |
| OSM L0 completeness estimate | Yes |
| B-end scan partner LOI | Yes (SLA draft per 9.6) |
| Heritage / UNESCO sites | If applicable + MOU draft (29.8) |
| Zone status | B only (no NVC) |

**Example candidate profile** (illustrative, not pre-selected):

```yaml
city_id: NOVA-CAND-001
name: "Example City"
country: XX
bbox: [lng_min, lat_min, lng_max, lat_max]
landmarks: 10  # UID placeholders after scan
osm_l0_gap_pct: 0.05
scan_partner: "Vendor LOI ref"
```

---

## Phase 2 — Community Review (14 days)

- Public forum thread per candidate  
- MGOC ethics + compliance pre-screen (veto only on legal red lines)  
- Technical committee scores feasibility (1–5) — published, not binding alone  

---

## Phase 3 — Weighted Vote (7 days)

Minimum **5,000 valid ballots** (founding period, DAU < 100k).

| Voter class | Weight | Eligibility |
|-------------|--------|-------------|
| Registered Novan (charter completed) | 40% | 1 vote per account |
| Verified contributor (≥1 CS record) | 30% | weighted by sqrt(contribution count), cap 10× |
| Tech + Product committee | 20% | internal ballot, published aggregate |
| MGOC ethics committee | 10% | compliance veto only |

**CITY-01 gates** (winner must pass all):

- OSM L0 gap ≤ 0.1% inside bbox  
- ≥10 landmarks feasible at CS≥70% within Phase 0 budget  
- B-end scan LOI signed  
- Zone B compliant (no NVC gateway)  

---

## Phase 4 — Notice & Lock (7 days)

1. Winning city published with bbox + landmark list  
2. 7-day objection period (formal appeal to MGOC)  
3. After lock: P0-01 evidence = governance log URL + `city-selection-record.json`  

```json
{
  "city_id": "NOVA-P0-CITY-001",
  "selected_at": "2026-XX-XX",
  "vote_totals_hash": "sha256:...",
  "bbox": [ ... ],
  "landmarks": [ ... ]
}
```

---

## Relation to Demo (40.7)

Demo environment **must** use the locked city bbox after Phase 4. Pre-lock demos may use provisional bbox with watermark.

---

## Checklist for Operators

- [ ] RFP published (3–5 cities)  
- [ ] MGOC pre-screen complete  
- [ ] ≥5,000 votes cast  
- [ ] Winner passes CITY-01  
- [ ] 7-day notice elapsed  
- [ ] P0-01 governance log entry  
- [ ] Demo spec updated (40.7)  

---

*Process ID: NOVA-CITY-SEL-v1.6*

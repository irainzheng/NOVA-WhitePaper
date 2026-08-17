# NOVA Digital Civilization — Executive Summary

**Version 1.6.0 · Governance & Simulation Edition**  
**Author**: rainzheng · © 2026 · CC BY-NC-ND 4.0

> *This is not a platform whitepaper—it is a constitution for a digital civilization.*

---

## One-Line Positioning

**NOVA** is a *reality-anchored, perpetually evolvable, habitable digital civilization*—a 3D world platform and the **Reference Implementation** of the **Avatar Sovereignty Protocol (ASP)**.

**Tagline**: *Reality as anchor, nova as light.*

---

## What NOVA Is

| Layer | Description |
|-------|-------------|
| **Physical anchor** | Crowdsourced digital twin of Earth (CS confidence scoring) |
| **Parallel worlds** | Builder-created universes with lifecycle & economics |
| **Digital persons** | DES tiers (bronze → silver → gold → research "consciousness stream") |
| **Governance** | Nova Civilization Charter (NCC-1.0), GPF pyramid, MGOC oversight |
| **Economy** | Dual rail: **NPT** (labor/points) + **NVC** (store-of-value, Phase 3+) |

NOVA explicitly **does not** promise biological consciousness upload. Gold DES is *advanced AI personality simulation* with COTMS provenance labeling.

---

## Minimum Viable Civilization (Phase 0)

**Scope**: Zone B only · **1 city · 10 landmarks · CS≥70%** · no NVC/AMM

| Milestone | Target |
|-----------|--------|
| L0 base | OSM + DEM, no gaps |
| Landmarks | 10 VR-enterable at gold CS |
| DAU | ≥5,000 at Phase 0 end |
| Compute γ | cost/revenue <50% for 30 days |
| Governance | Charter onboarding ≥80% |

City selection: **RFP → community vote → 7-day notice** (see `docs/phase0-city-selection.md`).

Budget envelope: **$2.3–5.3M** (whitepaper ch.40).

---

## Core Protocols

- **ASP** — export/import digital persons (CIP bundles); third-party invoke with TPR trust ratings  
- **CS-CHAIN** — on-chain contribution receipts for crowdsourcing anti-fraud  
- **COTMS** — consciousness origin traceability (O-0 … O-4 labels)  
- **DSNZ** — data sovereignty neutral zone (freeze, not delete)  
- **CIP** — civilization inheritance if platform winds down  

Conformance: 31 automated tests (`docs/asp-conformance-tests.yaml`). ASP Foundation governs spec from Phase 3.

---

## Economics (Simplified)

- **NPT**: catalog-anchored pricing; earn from contribution; destroy-on-spend (tiered β)  
- **NVC**: fixed 100B supply; AMM NPT↔NVC only in **Zone C** jurisdictions  
- **Revenue**: B2B data, virtual tourism, digital goods → later land economy & immortality subscription  
- **Stress test**: Monte Carlo on π (1–5% penetration), ARPU, compute γ — see `monte_carlo.py`

Neutral baseline: **1% immortality penetration**; 5% is optimistic ceiling for planning.

---

## Compliance Zones (NVC)

| Zone | NVC / Fiat | Notes |
|------|------------|-------|
| A | Full | Licensed jurisdictions |
| B | NPT only | Phase 0–2 default |
| C | NVC + AMM | Per-country rollout (public dashboard API) |
| D | Restricted | Geo-fence; assets safe on-chain |

---

## Top Risks & Mitigations

| Risk | Mitigation |
|------|------------|
| Compute cost > revenue | RPC priority stack; γ red/ yellow/ orange alerts |
| Cold start | One city deep; B2B scans for landmarks |
| Regulatory | Zone playbook; legal memos before Zone C |
| User expectation ("immortality") | DES limits + COTMS + marketing rules (FND-02) |
| Early governance centralization | 32.5 founding transition; weighted city vote |

---

## Engineering Package (`docs/`)

OpenAPI (ASP, Zone C dashboard), JSON Schemas, Phase 0 checklist, Demo spec, SLA/MOU templates, macro + Monte Carlo simulation, ASP Foundation charter.

**Status**: **Beta-ready** — documentation layer complete; Phase 0 engineering can start in parallel with city RFP.

---

## Contact

**rainzheng** · irainzheng@163.com

Full Chinese whitepaper: repository root HTML file.

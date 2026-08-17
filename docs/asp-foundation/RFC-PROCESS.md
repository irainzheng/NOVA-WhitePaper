# ASP RFC Process

> Whitepaper V1.7.0 · Section 19.10 · FND-01 / RFC-01 / RFC-02

---

## Overview

All **normative** changes to ASP (OpenAPI, JSON Schemas, conformance tests, CIP bundle layout) require an **RFC-ASP-NNN** document.

Until Phase 3, RFCs live in this monorepo under `docs/asp-foundation/rfcs/`. After ASP Foundation incorporation, migrate to `github.com/asp-foundation/spec`.

---

## States

| State | Meaning |
|-------|---------|
| **Draft** | PR open; not yet in comment period |
| **Comment** | 30-day public review |
| **Last Call** | 7-day final review |
| **Accepted** | Merged into spec |
| **Rejected** | Closed with rationale |
| **Withdrawn** | Author withdrew |

---

## Timeline

1. **Draft** — Author opens PR with `rfcs/RFC-ASP-NNN-title.md` from template  
2. **Comment (30d)** — Posted to governance log; Reference Implementation impact required  
3. **Last Call (7d)** — No blocking objections from TWG or MGOC liaison  
4. **Accepted** — Spec files updated; conformance tests added; version bump if needed  

---

## Version Rules (RFC-01)

| Change type | Version bump | Compatibility |
|-------------|--------------|---------------|
| Clarification only | patch | Immediate |
| Additive fields/endpoints | minor | 6 months backward compat |
| Breaking field/removal | major | 12 months + `426 Upgrade Required` |

---

## Roles

- **Author** — Any contributor  
- **TWG (Technical Working Group)** — Reviews technical soundness  
- **Reference Implementation** — NOVA team confirms implementability  
- **MGOC Liaison** — Ethics/marketing impact (FND-02)  

---

## File Naming

```
docs/asp-foundation/rfcs/
├── RFC-ASP-000-template.md
├── RFC-ASP-001-export-manifest-v0.1.md   # example
└── README.md
```

---

## Blocking Objection

A **blocking objection** must include:

1. Specific spec text concern  
2. Alternative proposal or migration path  
3. TWG member or MGOC liaison signature  

Non-blocking feedback does not extend Last Call.

---

*Process ID: ASP-RFC-v1.7*

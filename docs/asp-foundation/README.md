# ASP Foundation

> Whitepaper V1.6.0 · Section 19.9  
> Avatar Sovereignty Protocol — independent governance from Phase 3

---

## Mission

Maintain ASP as an **open standard** for digital avatar sovereignty, portability (CIP), and third-party invocation— independent of any single platform instance.

NOVA is the **Reference Implementation** until the Foundation assumes spec stewardship.

---

## Repository Structure (planned independent org)

```
asp-foundation/
├── CHARTER.md              # This document
├── certification/
│   └── process.md
├── spec/
│   ├── openapi.yaml        # synced from NOVA docs/asp-openapi.yaml
│   ├── conformance-tests.yaml
│   └── schemas/
├── rfcs/                   # RFC-ASP-NNN
└── implementations/
    └── registry.json       # Certified / Compatible implementations
```

**FND-01**: Spec changes require RFC + 30-day public comment before merge.

---

## Governance Bodies

| Body | Role | Term |
|------|------|------|
| **Board of Directors** (5–9) | Strategy, budget, appoint working groups | 2 years |
| **Technical Working Group** | OpenAPI, Schema, conformance tests | rolling |
| **Certification Working Group** | Third-party testing & badges | rolling |
| **MGOC Liaison** | Annual audit, ethics veto on marketing misuse | ex officio |

Transition: Phase 3 NVC mainnet launch triggers Foundation incorporation (jurisdiction TBD, Singapore/EU candidates per 22.6).

---

## Funding

- NOVA team endowment (Phase 0–2)  
- Certification fees (cost-recovery, non-profit cap)  
- Grants (digital identity / heritage preservation)  

No Foundation token; no NVC allocation to Foundation board members (conflict policy).

---

## Relationship to NOVA

| Aspect | Foundation | NOVA Platform |
|--------|------------|---------------|
| Spec ownership | Yes (Phase 3+) | Reference Implementation |
| CIP export format | Defines | Implements first |
| User accounts | No | Yes |
| DES marketing | Sets COTMS rules | Must comply |

---

See [certification-process.md](./certification-process.md) for badge criteria.

*Charter draft v1.6 · subject to legal incorporation*

# ASP Third-Party Certification Process

> Whitepaper V1.6.0 · Section 19.9 · CON-01 / CON-02 / FND-02

---

## Badge Levels

| Badge | Requirement | Renewal |
|-------|-------------|---------|
| **ASP Compatible** | ≥90% conformance tests pass; ASP-SECURITY no FAIL | Annual self-attestation + spot check |
| **ASP Certified** | 100% pass + independent security audit | Annual full retest |

Tests defined in `docs/asp-conformance-tests.yaml` (31 cases, 4 suites).

---

## Application Flow

```
Applicant → Self-test (public CI) → Submit report → Certification WG review
    → (Certified only) Security audit → Board register → Public listing
```

**Timeline**: Compatible ~4 weeks; Certified ~12 weeks (audit dependent).

---

## Submission Package

1. Implementation URL + `asp_version` supported  
2. CI log (all suites) with commit SHA  
3. Contact + security disclosure policy  
4. Marketing copy sample (FND-02 review)  
5. (Certified) Audit report < 12 months old  

---

## Revocation

Immediate revoke if:

- Marketing claims consciousness upload beyond COTMS labels  
- Security FAIL in spot check  
- User data lock-in (export denied without cause)  

Appeal window: 30 days to Certification WG.

---

## Reference Implementation (NOVA)

- Must pass **100%** before each NOVA minor release  
- Public CI badge linked from governance log  
- Does not auto-grant Certified status to third parties  

---

## Registry Entry (public JSON)

```json
{
  "implementation_id": "example-asp-server",
  "badge": "compatible",
  "asp_version": "0.1.0",
  "certified_at": "2026-XX-XX",
  "expires_at": "2027-XX-XX",
  "report_url": "https://..."
}
```

---

*Process ID: ASP-CERT-v1.6*

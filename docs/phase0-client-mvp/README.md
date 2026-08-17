# nova-client-phase0 — MVP Specification

> Whitepaper V1.7.0 · Section 40.10 · MVP-01 / MVP-02

Planned open-source repository for Phase 0 roam + crowdsourced upload client.

---

## Goals

1. **L0–L2 city roam** in selected benchmark city  
2. **VR enter** 10 landmarks at CS≥70%  
3. **Crowd upload** → CS pipeline observable in UI (&lt;5 min P0-04)  
4. **Zone B** only — no NVC/AMM surfaces  
5. **Charter gate** — onboarding requires NCC study completion (P0-08)  

---

## Repository Layout (planned)

```
nova-client-phase0/
├── LICENSE                 # Apache-2.0
├── README.md               # links to whitepaper commit SHA (MVP-01)
├── package.json
├── apps/
│   └── web/                # primary WebGL client
├── packages/
│   ├── renderer/           # CesiumJS / Three.js tiles loader
│   ├── cs-upload/          # upload + progress UI
│   └── nova-sdk/           # typed API client (OpenAPI gen)
├── docs/
│   └── ARCHITECTURE.md
└── .github/
    └── workflows/
        ├── ci.yml
        └── sync-whitepaper-ref.yml
```

---

## Tech Stack

| Layer | Choice | Rationale |
|-------|--------|-----------|
| Web client | React + TypeScript | Ecosystem, hiring |
| Globe | CesiumJS | L0 OSM/DEM native |
| Landmark VR | Three.js + 3D Tiles | Fine control for CS≥70% assets |
| API | OpenAPI-generated client | Matches docs/asp-openapi patterns |
| Auth | OAuth2 PKCE | Zone B accounts |
| i18n | en + zh | Matches whitepaper EN mirror |

---

## Non-Goals (Phase 0)

- Native mobile apps (Web-first)  
- Gold DES / real-time avatar (Phase 4)  
- NVC wallet  
- Parallel world builder (Phase 2)  

---

## Acceptance Mapping

| Checklist | Client responsibility |
|-----------|----------------------|
| P0-02 | Render 10 landmarks; show CS badge |
| P0-04 | Upload UI + pipeline timer telemetry |
| P0-06 | Hide NVC/AMM routes |
| P0-08 | Charter quiz gate before roam |
| P1-03 | Demo build flag + watermark |
| P1-06 | CI runs `docs/ci/sync_check.py` on docs submodule pin |

---

## Getting Started (when repo exists)

```bash
git clone https://github.com/novaverse/nova-client-phase0  # planned
cd nova-client-phase0
npm install
npm run dev
# Configure .env: NOVA_API_BASE, NOVA_CITY_BBOX
```

---

See [ARCHITECTURE.md](./ARCHITECTURE.md) for module diagram.

*Spec ID: NOVA-CLIENT-P0-v1.7*

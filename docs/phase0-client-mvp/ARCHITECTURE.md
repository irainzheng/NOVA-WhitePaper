# Phase 0 Client Architecture

> V1.7.0 · MVP-02

```
┌─────────────────────────────────────────────────────────┐
│                    Web App (React)                       │
│  ┌─────────────┐  ┌──────────────┐  ┌───────────────┐ │
│  │ CharterGate │  │ RoamViewport │  │ UploadPanel   │ │
│  └──────┬──────┘  └──────┬───────┘  └───────┬───────┘ │
└─────────┼─────────────────┼──────────────────┼─────────┘
          │                 │                  │
          ▼                 ▼                  ▼
   ┌────────────┐   ┌─────────────┐   ┌─────────────────┐
   │ Auth OAuth │   │  Renderer   │   │  cs-upload pkg  │
   └─────┬──────┘   │ Cesium+Three│   └────────┬────────┘
         │          └──────┬──────┘            │
         │                 │                   │
         └────────────┬────┴───────────────────┘
                      ▼
              ┌───────────────┐
              │   nova-sdk    │  ← OpenAPI / REST
              └───────┬───────┘
                      ▼
              ┌───────────────┐
              │  NOVA API     │  (backend — closed source OK)
              │  Zone B       │
              └───────────────┘
```

## Data Flow — Upload (P0-04)

1. User selects video/photos → `cs-upload` chunks to API  
2. Poll `GET /cs/jobs/{id}` until `status=scored`  
3. Client logs `scored_at - submitted_at` (must be &lt;5 min P95)  
4. On success, refresh tile layer for affected UID  

## Rendering Layers

| Layer | Engine | Source |
|-------|--------|--------|
| L0–L2 city | CesiumJS | OSM + DEM + 3D Tiles base |
| Landmarks | Three.js | Vendor scan tiles (40.9) |
| CS badge | UI overlay | DTA API |

## Security

- No API keys in client bundle (PKCE only)  
- Sandbox vs prod via `NOVA_ENV`  
- Upload size cap 500MB / file (Demo: 100MB)  

## CI

- `npm test` + ESLint  
- Optional: link to whitepaper SHA in README on release tag  

*Architecture v1.7*

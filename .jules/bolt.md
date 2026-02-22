## 2026-02-21 - [Initial Performance Assessment]
**Learning:** Found redundant connection creation for `httpx.AsyncClient` in `web.py` and double-loading of `partners.json` in the `/api/partners` endpoint.
**Action:** Implement connection pooling via FastAPI lifespan and optimize data flow to reuse already loaded partner data.

## 2026-02-21 - [FastAPI Shim Considerations]
**Learning:** The codebase uses a custom FastAPI shim for environments without the full library. Direct use of new FastAPI features like `lifespan` or `app.state` can break compatibility with this shim if not handled defensively.
**Action:** Always use `getattr(request.app, "state", None)` or similar defensive checks when relying on newer FastAPI features to ensure the application remains compatible with the test shim.

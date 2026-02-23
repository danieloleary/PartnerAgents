# Performance Optimizations (Bolt) - 2026-02-22

## Key Optimizations

### 1. In-memory Caching in `partner_state.py`
- **Issue:** Every call to `list_partners`, `get_partner`, or `get_partner_stats` triggered a disk read and JSON parse of `partners.json`.
- **Solution:** Implemented a global `_partners_cache` and `_stats_cache`.
- **Validation:** Added `os.path.getmtime` check to ensure the cache is invalidated if the file is modified externally.
- **Results:** Profiling showed a reduction in execution time for 100 operations from 0.131s to 0.004s.

### 2. $O(1)$ Lookup for Partners
- **Issue:** `get_partner` performed a linear search through the list of partners.
- **Solution:** Added a dictionary-based index `_partners_by_name` that is populated whenever the partners list is loaded.

### 3. Connection Pooling in `web.py`
- **Issue:** `call_llm` created a new `httpx.AsyncClient` for every request, incurring significant overhead for connection setup and teardown.
- **Solution:** Implemented a shared `httpx.AsyncClient` stored in `app.state`, managed by a FastAPI `lifespan` event handler.
- **Compatibility:** Added defensive checks for `app.state` to ensure compatibility with the project's lightweight FastAPI shim.

### 4. Efficient Rate Limiting
- **Issue:** The rate limiter used list comprehensions to prune old timestamps, which is $O(n)$ and can be slow under high load.
- **Solution:** Switched to `collections.deque` for $O(1)$ pruning from the left using `popleft()`.

## Lessons Learned
- **Shim Compatibility:** When modifying core library behavior (like adding `lifespan`), ensure the project's test shims are updated accordingly to avoid CI/CD failures.
- **Defensive Programming:** Using `getattr(request.app, 'state', None)` is essential when the execution environment might not fully support the FastAPI spec.

## 2026-02-23 - Compression & LRU Hardening
**Learning:** Monolithic HTML responses and unbounded in-memory caches are silent performance killers. GZip reduced the home page payload from 30KB to 7KB (76% saving). Unbounded dicts for caching and rate limiting can lead to memory exhaustion; using `OrderedDict` with `popitem(last=False)` provides O(1) LRU pruning.
**Action:** Always enable response compression for static/monolithic payloads and implement explicit size limits on all in-memory caches using OrderedDict or similar LRU patterns.

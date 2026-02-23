---
title: Sentinel's Journal - Critical Security Learnings
keywords: ["partner management vulnerability", "application was vulnerable", "monolithic string within", "csrf like attacks", "rendered using innerhtml", "partners json"]
---
# Sentinel's Journal - Critical Security Learnings

## 2025-05-15 - Stored XSS in Partner Management
**Vulnerability:** The application was vulnerable to Stored Cross-Site Scripting (XSS). User-provided partner names and emails were stored unsanitized in `partners.json` and rendered using `innerHTML` in the FastAPI-based web interface (`web.py`).
**Learning:** Embedding complex HTML/JS as a monolithic string within a Python file (`web.py`) obscures vulnerabilities from standard static analysis tools and makes manual review harder. Developers may mistakenly trust backend data when it's easily accessible via a shared state module like `partner_state.py`.
**Prevention:** Always escape dynamic content on both the backend (producer) and frontend (consumer). Use `textContent` or similar DOM-safe methods instead of `innerHTML` for dynamic values. Implement input validation and sanitization at the API boundary.

## 2025-05-15 - Insecure CORS Configuration
**Vulnerability:** `CORSMiddleware` was configured with `allow_origins=["*"]` and `allow_credentials=True`.
**Learning:** This is an insecure combination that is rejected by modern browsers and can lead to CSRF-like attacks if sensitive data is involved.
**Prevention:** When using wildcard origins (`*`), always set `allow_credentials=False`. If credentials are required, specific origins must be listed.

## 2026-02-21 - Insufficient Chat Input Sanitization & DoS Risk
**Vulnerability:** The `web.py` chat interface used a weak blacklist approach (`.replace("<script", "")`) that was easily bypassed and not even applied to the final LLM payload. Additionally, the in-memory rate limiter was vulnerable to memory exhaustion as it never purged unique IP entries.
**Learning:** Sanitization must be an "active" part of the data flow, not a side-effect that is ignored. Blacklisting specific tags is insufficient against modern XSS vectors. In-memory stores for request tracking must have bounds or expiration logic to prevent DoS.
**Prevention:** Use regex-based tag stripping or established sanitization libraries on both input (LLM protection) and output (XSS protection). Implement pruning logic for in-memory state objects to prevent unbounded growth.

## 2026-02-23 - Hardened Web UI and Cache Isolation
**Vulnerability:** The Web UI lacked critical security headers (CSP, X-Frame-Options), had no request body size limits, and was vulnerable to cross-user cache exposure because LLM response cache keys did not include user-specific identifiers (API keys).
**Learning:** In a multi-user environment sharing a single process (like the monolithic `web.py`), global caches must be partitioned by user or session data (e.g., hashed API keys) to prevent data leakage. Minimal framework shims can cause CI/CD failures if they don't support the decorators used in the application code.
**Prevention:** Implement a central security middleware for all incoming requests to enforce global policies (headers, limits). Always include a user-specific salt or identifier in cache keys for sensitive data.

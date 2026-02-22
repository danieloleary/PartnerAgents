# Sentinel's Journal - Critical Security Learnings

## 2025-05-15 - Stored XSS in Partner Management
**Vulnerability:** The application was vulnerable to Stored Cross-Site Scripting (XSS). User-provided partner names and emails were stored unsanitized in `partners.json` and rendered using `innerHTML` in the FastAPI-based web interface (`web.py`).
**Learning:** Embedding complex HTML/JS as a monolithic string within a Python file (`web.py`) obscures vulnerabilities from standard static analysis tools and makes manual review harder. Developers may mistakenly trust backend data when it's easily accessible via a shared state module like `partner_state.py`.
**Prevention:** Always escape dynamic content on both the backend (producer) and frontend (consumer). Use `textContent` or similar DOM-safe methods instead of `innerHTML` for dynamic values. Implement input validation and sanitization at the API boundary.

## 2025-05-15 - Insecure CORS Configuration
**Vulnerability:** `CORSMiddleware` was configured with `allow_origins=["*"]` and `allow_credentials=True`.
**Learning:** This is an insecure combination that is rejected by modern browsers and can lead to CSRF-like attacks if sensitive data is involved.
**Prevention:** When using wildcard origins (`*`), always set `allow_credentials=False`. If credentials are required, specific origins must be listed.

## 2025-05-15 - Authentication Bypass via Cache
**Vulnerability:** The LLM response cache in `web.py` used only the user's message as a hash key. This allowed a user with no API key (or an invalid one) to receive a response that was originally fetched and cached by a user with a valid API key.
**Learning:** Caching logic must always account for the security context (authentication/authorization) if the result of the operation depends on it.
**Prevention:** Include a hash of the authentication token or user ID in any cache keys for operations that require authentication.

## 2025-05-15 - DoS via Large Payloads
**Vulnerability:** The application had no limit on the size of JSON payloads sent to `POST` endpoints, making it vulnerable to memory exhaustion (OOM) attacks.
**Learning:** Default framework settings (like Starlette/FastAPI) often don't enforce strict body size limits.
**Prevention:** Implement a middleware to check `Content-Length` and reject payloads exceeding a reasonable threshold (e.g., 1MB).

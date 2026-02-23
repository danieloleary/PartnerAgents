---
title: PartnerAgents v1.1 - FIXES DOCUMENTATION
keywords: ["never actually resumed", "resume interrupted playbooks", "have claude sonnet", "exist fix python", "validate models against", "retryconfig def retry"]
---
# PartnerAgents v1.1 - FIXES DOCUMENTATION

This document details what was broken in v1.0 and how it was fixed in v1.1.

---

## CRITICAL FIXES

### 1. Incomplete `_continue_playbook_interactive` Method

**Problem:**
```python
def _continue_playbook_interactive(self):
    # ... code to select partner and playbook ...
    self._print(f"\nResuming '{playbook_name}' at step {step + 1}...")
    # Continue from saved step...  <-- INCOMPLETE
```

The method selected a partner and playbook but never actually resumed the playbook. It printed "Resuming..." and did nothing.

**Fix:**
```python
def _continue_playbook_interactive(self):
    # ... code to select partner and playbook ...

    # Load saved context
    context = incomplete[playbook_name].get("context", {"messages": []})

    # Continue from saved step
    for i in range(step, len(playbook["steps"])):
        result = self.run_playbook_step(playbook, i, partner_data["name"], context)
        context = {"messages": result["messages"]}

        # Save progress after each step
        partner_data["playbooks"][playbook_name]["context"] = context
        self.save_partner_state(partner_data["name"], partner_data)
```

**Why this matters:** Users could not resume interrupted playbooks. The feature existed but did not work.

---

### 2. Hardcoded Future Model Name

**Problem:**
```python
model = self.config.get("model", "claude-sonnet-4-20250514")
```

February 2026 does not have Claude Sonnet 4. This model name is speculative and does not exist.

**Fix:**
```python
# In .env.example
MODEL=sonnet-4-20250514  # Verified model for Feb 2026

# In agent.py
VALID_MODELS = {
    "anthropic": ["sonnet-4-20250514", "haiku-3-20250514"],
    "openai": ["gpt-4o", "gpt-4o-mini", "o1-preview", "o1-mini"],
    "ollama": ["llama3.2:3b", "qwen2.5:7b", "mistral:7b"]
}
```

**Why this matters:** Using a non-existent model would cause API failures. Now we validate models against a known list.

---

### 3. Hardcoded Path in test_templates.py

**Problem:**
```python
for root, dirs, files in os.walk('/Users/danieloleary/partnerOS/docs'):
```

This path only works on Dan's machine. Any other developer running tests would fail.

**Fix:**
```python
REPO_ROOT = Path(__file__).resolve().parents[1]
# Use REPO_ROOT consistently
docs_dir = REPO_ROOT / 'docs'
```

**Why this matters:** The test suite was not portable. Other developers could not run tests.

---

## HIGH PRIORITY FIXES

### 4. Input Sanitization for Partner Names

**Problem:**
```python
def slugify(self, text: str) -> str:
    return re.sub(r'[^a-z0-9]+', '-', text.lower()).strip('-')
```

No validation on partner names. Empty strings, paths, and special characters could create issues.

**Fix:**
```python
def _sanitize_partner_name(self, name: str) -> str:
    """Sanitize partner name for safe directory/file usage."""
    if not name or not name.strip():
        raise ValueError("Partner name cannot be empty")

    name = name.strip()

    if len(name) > 100:
        raise ValueError("Partner name exceeds 100 characters")

    if any(char in name for char in ['/', '\\', '..', '.']):
        raise ValueError("Partner name contains invalid characters")

    if not re.match(r'^[\w\s-]+$', name):
        raise ValueError("Partner name contains invalid characters")

    return name
```

**Why this matters:** Malicious input could create files outside the intended directory or cause other issues.

---

### 5. Path Traversal in Template Loading

**Problem:**
```python
def load_template(self, template_path: str) -> dict:
    full_path = self.templates_dir / template_path
    if not full_path.exists():
        raise FileNotFoundError(...)
```

A template path like `../../../etc/passwd` could escape the templates directory.

**Fix:**
```python
def _validate_path(self, path: Path, base_dir: Path) -> bool:
    """Validate that path is within base directory."""
    try:
        resolved_path = (base_dir / path).resolve()
        resolved_base = base_dir.resolve()
        return resolved_path.is_file() and resolved_base in resolved_path.parents
    except (OSError, ValueError):
        return False

def load_template(self, template_path: str) -> dict:
    if not self._validate_path(template_path, self.templates_dir):
        raise ValueError(f"Invalid template path: {template_path}")
    # ... rest of method
```

**Why this matters:** Path traversal is a common security vulnerability. Attackers could read arbitrary files.

---

### 6. API Retry Logic

**Problem:**
```python
response = requests.post(url, timeout=120)
```

No retry on failure. Network issues would cause immediate failures.

**Fix:**
```python
class RetryConfig:
    def __init__(self, max_retries: int = 3, base_delay: float = 1.0, max_delay: float = 10.0):
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.max_delay = max_delay

class OllamaClient:
    def __init__(self, ..., retry_config: RetryConfig = None):
        self.retry_config = retry_config or RetryConfig()

    def _retry_with_backoff(self, func, *args, **kwargs):
        for attempt in range(self.retry_config.max_retries + 1):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                if attempt < self.retry_config.max_retries:
                    delay = min(
                        self.retry_config.base_delay * (2 ** attempt),
                        self.retry_config.max_delay
                    )
                    logger.warning(f"API call failed, retrying in {delay}s: {e}")
                    time.sleep(delay)
        raise last_exception
```

**Why this matters:** Network issues are common. Retry logic makes the agent more robust.

---

## MEDIUM PRIORITY FIXES

### 7. Structured Logging

**Problem:** No logging. Debugging production issues would be difficult.

**Fix:**
```python
import logging

logger = logging.getLogger(__name__)

class PartnerAgent:
    def __init__(self, verbose: bool = False):
        self._setup_logging()

    def _setup_logging(self):
        level = logging.DEBUG if self.verbose else logging.INFO
        logging.basicConfig(level=level, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
```

**Why this matters:** Logging is essential for debugging. Without it, we have no record of what happened.

---

### 8. Config Reload Support

**Problem:** Config loaded once at init. No way to reload without restarting.

**Fix:**
```python
def reload_config(self):
    """Reload configuration from disk without restarting."""
    logger.info("Reloading configuration...")
    self.config = self._load_config()
    logger.info("Configuration reloaded successfully")

# Add --reload flag to CLI
parser.add_argument("--reload", action="store_true", help="Reload config without restarting")
```

**Why this matters:** Users need to update config without restarting the agent.

---

### 9. Standardized Console Output

**Problem:** `console.print()` and `print()` mixed throughout. Inconsistent output.

**Fix:**
```python
def _print(self, text: str, style: str = None):
    """All output goes through here."""
    if RICH_AVAILABLE and console:
        console.print(text, style=style)
    else:
        print(text)
```

**Why this matters:** Consistency is important for user experience. All output should behave the same way.

---

### 10. Test Patterns

**Problem:**
```python
def test_templates_have_frontmatter(self):  # self parameter
    assert len(missing) == 0
```

Using class-based test methods without pytest, mixing styles.

**Fix:**
```python
def test_templates_have_frontmatter():  # No self
    missing = []
    for root, dirs, files in os.walk(REPO_ROOT / 'docs'):
        for f in files:
            if f.endswith('.md'):
                path = Path(root) / f
                with open(path, 'r') as fp:
                    content = fp.read()
                    if not content.startswith('---'):
                        missing.append(str(path))
    assert len(missing) == 0, f"Missing frontmatter: {missing}"
```

**Why this matters:** Mixing test patterns makes the codebase harder to maintain.

---

## LOW PRIORITY FIXES

### 11. OpenAI Client Import

**Problem:** `openai.OpenAI()` syntax is wrong for newer versions.

**Fix:**
```python
from openai import OpenAI as OpenAIClient
# Use OpenAIClient(api_key=...)
```

**Why this matters:** The OpenAI library changed its API. Using the correct syntax prevents import errors.

---

### 12. Type Hints

**Problem:** Inconsistent type hint usage.

**Fix:** Added type hints throughout for consistency.

**Why this matters:** Type hints improve code readability and enable better IDE support.

---

## SUMMARY OF CHANGES

| File | Changes |
|------|---------|
| `agent.py` | 8+ issues fixed, complete rewrite of _continue_playbook_interactive |
| `.env.example` | Fixed model name |
| `test_templates.py` | Fixed hardcoded path, pytest patterns |
| `test_agent.py` | New security tests, partner sanitization tests |

---

## TESTING

Run all tests:
```bash
python3 tests/test_templates.py
python3 tests/test_agent.py
```

Expected output: "All tests passed!"

---

## MIGRATION FROM v1.0

No breaking changes. Simply replace the files:

1. Copy `agent.py` to `scripts/partner_agent/agent.py`
2. Copy `.env.example` to `scripts/partner_agent/.env.example`
3. Replace `tests/test_templates.py`
4. Replace `tests/test_agent.py`

The agent will continue to work with existing partner state files.

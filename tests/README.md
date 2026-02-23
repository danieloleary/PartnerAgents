---
title: PartnerAgents Test Suite
keywords: ["overall site structure", "tier which tiers", "skills gained what", "tests validate", "validation tests", "every push"]
---
# PartnerAgents Test Suite

This directory contains automated tests for PartnerAgents.

## Running Tests

```bash
# Run all tests (recommended)
pytest tests/ -v

# Run specific test file
pytest tests/test_templates.py -v
pytest tests/test_agent.py -v

# Run with Python directly
python3 tests/test_templates.py
python3 tests/test_agent.py
```

## Test Categories

### Tier 1 - Critical (Must Pass)
These tests validate core template structure and are required to pass before any merge.

| Test | Purpose |
|------|---------|
| `test_templates_exist` | Verifies at least 1 template exists |
| `test_templates_have_frontmatter` | All .md files have YAML frontmatter |
| `test_frontmatter_schema_validation` | All templates have 17 required fields |
| `test_template_count_per_category` | Correct template counts per folder |
| `test_folder_structure` | All required directories exist |
| `test_playbook_template_references` | Playbooks reference existing templates |
| `test_frontmatter_yaml_parseable` | No YAML syntax errors |

### Tier 2 - Site/Docs/Architecture
These tests validate the overall site structure and configuration.

| Test | Purpose |
|------|---------|
| `test_config_yaml_valid` | config.yaml has required fields |
| `test_playbook_yaml_schema` | All playbooks have valid schema |
| `test_no_duplicate_template_titles` | No duplicate template titles |
| `test_template_files_have_content` | Templates have meaningful content |
| `test_starlight_build_succeeds` | Starlight builds without errors |
| `test_astro_config_valid` | astro.config.mjs is valid |

### Agent Tests
Security and validation tests for the Partner Agent.

| Test | Purpose |
|------|---------|
| `test_agent_import` | agent.py compiles without errors |
| `test_env_example_exists` | .env.example has required variables |
| `test_partner_sanitization` | Partner name validation works |
| `test_path_validation` | Path traversal attacks prevented |
| `test_slugify` | URL slug generation works |

## Test Requirements

### Frontmatter Schema (17 fields)
Every template must have these fields:
- `title` - Display name
- `section` - Category section
- `category` - Type (legal, operational, strategic, etc.)
- `template_number` - Unique identifier (e.g., "L.1", "F.1")
- `version` - Semantic version
- `last_updated` - Date (YYYY-MM-DD)
- `author` - Who created/owns it
- `tier` - Which tiers can use (Bronze, Silver, Gold)
- `skill_level` - beginner, intermediate, advanced
- `purpose` - tactical, strategic, operational
- `phase` - lifecycle phase
- `time_required` - Estimated completion time
- `difficulty` - easy, medium, hard
- `prerequisites` - What to complete first
- `description` - Brief summary
- `purpose_detailed` - Full explanation
- `outcomes` - What you get from using it
- `skills_gained` - What you learn

### Template Count Per Category
| Category | Count |
|----------|-------|
| strategy | 8 |
| recruitment | 10 |
| enablement | 7 |
| agent | 4 |
| getting-started | 3 |
| resources | 2 |
| legal | 4 |
| finance | 1 |
| security | 1 |

## Adding New Tests

When adding new tests:
1. Add to appropriate test file (`test_templates.py` or `test_agent.py`)
2. Use descriptive names: `test_<what>_<validates>`
3. Include docstrings explaining what the test does
4. Run `pytest tests/ -v` to verify

## CI Integration

Tests run automatically on:
- Every push to main
- Every Pull Request
- Can be run manually via GitHub Actions

## Troubleshooting

### Test fails: "Missing frontmatter"
The template file doesn't start with `---`. Add YAML frontmatter.

### Test fails: "Missing fields"
Run `python3 scripts/standardize_templates.py` to auto-add missing fields.

### Test fails: "Template not found"
Check that playbook template references point to existing files in `docs/`.

### All tests pass but expected to fail
Check that you're running from the repo root: `pytest tests/ -v`

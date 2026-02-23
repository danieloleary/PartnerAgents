# Jules Configuration for PartnerAgents

## Project Context
PartnerAgents is a complete playbook system for building and scaling strategic partnerships with AI-powered automation. It includes:
- 67 Markdown documentation templates (Starlight/Astro)
- 14 Agent-First Templates (skill cards + workflows)
- Python AI Partner Agent (Ollama, Anthropic, OpenAI, OpenRouter)
- 7 automation playbooks
- Web UI with chat interface
- 163 tests (pytest)

## Key Commands

### Run Tests
```bash
cd PartnerAgents/PartnerAgents
pytest tests/ -v
```

### Run Web UI
```bash
cd PartnerAgents/PartnerAgents
python3 scripts/partner_agents/web.py
```

### Build Docs
```bash
cd PartnerAgents/PartnerAgents/partneros-docs
npm run build
```

### Run Linter
```bash
cd PartnerAgents/PartnerAgents
python3 scripts/lint_markdown.py
```

## Test Expectations
- All 163 tests should pass
- 96 pages should build
- No markdown lint errors

## Common Tasks
- Adding tests: Add to tests/test_*.py
- Adding templates: Add to partneros-docs/src/content/docs/
- Web UI changes: Edit scripts/partner_agents/web.py

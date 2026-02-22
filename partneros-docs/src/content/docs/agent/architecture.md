---
title: System Architecture
category: strategic
version: 1.0.0
author: PartnerOS Team
tier:
skill_level: advanced
purpose: strategic
phase: strategy
time_required: 1 hour
difficulty: medium
prerequisites:
description: Overview of the PartnerOS multi-agent system architecture and state management
outcomes:
  - Understand the Orchestrator/Driver pattern
  - Identify technical debt and scaling paths
skills_gained:
  - System Design
  - Multi-agent coordination
keywords: ["architecture review", "multi-agent system", "state management", "orchestrator", "technical debt"]
---

# PartnerOS System Architecture Review

*Date: May 22, 2024*

## Overview

PartnerOS currently consists of two distinct agent systems that share some conceptual goals but have diverged in implementation:

1.  **CLI Agent (`scripts/partner_agent/`)**: A robust, single-agent system designed for interactive playbook execution via the terminal.
2.  **Web/Multi-Agent System (`scripts/partner_agents/`)**: A FastAPI-based web interface and an Orchestrator/Driver framework for a multi-agent team.

---

## Component Analysis

### 1. CLI Agent (`partner_agent/`)
- **Main Entry**: `agent.py`
- **State Management**: Uses `partner_state.py` (CLI version) and a directory-per-partner structure in `state/`.
- **Logic**: Implements a `PartnerAgent` class that handles playbook loading, template parsing, and LLM interaction.
- **Strengths**:
    - Deep integration with Markdown templates in `docs/`.
    - Robust state persistence for complex, multi-step playbooks.
    - Path traversal security for template and playbook loading.

### 2. Multi-Agent Framework (`partner_agents/`)
- **Orchestrator**: `orchestrator.py` manages a fleet of specialized "Drivers".
- **Drivers**: Specialized agents (Owner, Strategist, etc.) defined in `drivers/` with specific roles and skills.
- **Metaphor**: Uses an "F1 Race Team" metaphor (Race Engineer, Pit Stops, Telemetry).
- **Web UI**: `web.py` provides a FastAPI backend and a monolithic HTML/JS frontend.

---

## State Management Comparison

| Feature | CLI Agent (`partner_agent`) | Web/Multi-Agent (`partner_agents`) |
| :--- | :--- | :--- |
| **Storage Format** | Directory per partner (slugified) | Single `partners.json` file |
| **Metadata File** | `metadata.json` per partner | Combined list in one file |
| **State Class** | `PartnerState` (Object-oriented) | Functional `partner_state.py` |
| **Lifecycle Tracking** | Stages (Prospect -> Strategic) | Simple status string |
| **Playbook Progress**| Detailed step-by-step tracking | Not currently tracked in JSON |

---

## Technical Debt

### 1. Divergent State Management
The project maintains two separate `partner_state.py` implementations. This leads to "split-brain" where partners added via the Web UI don't show up in the CLI and vice-versa.

### 2. Bypassed Orchestration in Web UI
While `partner_agents/` defines a sophisticated Orchestrator and Driver system, `web.py` currently bypasses it. The `/chat` endpoint calls a monolithic `call_llm` function with a system prompt that *emulates* the multi-agent team rather than actually dispatching tasks to the Drivers.

### 3. Monolithic Frontend
The entire Web UI (HTML, CSS, JavaScript) is stored as a single raw string within `web.py`. This makes frontend development, testing, and maintenance extremely difficult.

### 4. Scaling Bottlenecks
- **`partners.json`**: Storing all partners in a single JSON file will lead to performance and concurrency issues as the partner count grows.
- **In-memory store**: Rate limiting and caching in `web.py` are in-memory, meaning they won't persist across restarts or work in a multi-worker environment.

### 5. Redundant Logic
The `PartnerAgent` class in `agent.py` contains its own state-handling methods (`get_partner_state`, `save_partner_state`) that partially duplicate functionality in its own `partner_state.py`.

---

## Detailed Analysis: CLI Agent (`agent.py`)

The `PartnerAgent` class is the heart of the CLI system but suffers from "God Object" tendencies:

- **Responsibilities**: It handles UI (rich console output), configuration, LLM client initialization, template parsing, state management, and playbook orchestration.
- **Scalability**: While excellent for a single-user CLI tool, the tight coupling between UI and logic makes it difficult to reuse the playbook engine in the Web UI.
- **Security**: It implements good path-traversal protections (`_validate_path`) and input sanitization (`_sanitize_partner_name`).
- **Resilience**: The `OllamaClient` includes an exponential backoff retry mechanism, which is a solid architectural decision for dealing with local LLM instability.

---

## Recommendations for Scalability & Architecture

### 1. Unified State Layer
- Adopt a single, unified `PartnerState` implementation.
- Move from flat files to a database (e.g., SQLite for local, PostgreSQL for cloud) to support concurrent access and complex queries.
- Ensure both CLI and Web interfaces use the same persistence layer.

### 2. Real Orchestration
- Refactor `web.py` to use the `Orchestrator` to dispatch user requests.
- Implement a "Router" driver that classifies user intent and hands off to the appropriate specialized agent.

### 3. Frontend/Backend Separation
- Extract the HTML/JS/CSS from `web.py` into a modern frontend framework (e.g., React, Vue) or at least into separate static files.
- Use FastAPI's `StaticFiles` and template engines (like Jinja2) if staying with server-side rendering.

### 4. Shared Configuration
- Create a unified `config.yaml` that both systems read from.
- Centralize the "Company Context" so changes to the product or value prop are reflected everywhere.

### 5. Playbook Engine as a Service
- Extract the playbook execution logic from the CLI `PartnerAgent` into a shared service/module that the Web UI can also utilize to guide users through structured workflows.

### 6. Multi-Agent Scalability
- **Asynchronous Execution**: Transition the Orchestrator and Drivers to use `asyncio` for all calls to prevent I/O blocking during LLM requests.
- **Distributed Agents**: For high-load scenarios, consider moving from in-process drivers to microservices or serverless functions coordinated via an event bus (e.g., Redis Pub/Sub, RabbitMQ).
- **Stateless Orchestration**: Ensure the Orchestrator can recover session state from a shared store so that user interactions can be handled by any available server instance.

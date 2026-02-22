---
title: Agent Setup
category: operational
version: 1.0.0
author: PartnerOS Team
tier: 
skill_level: intermediate
purpose: operational
phase: operational
time_required: 1-2 hours
difficulty: easy
prerequisites: 
description: Install and configure the Partner Agent
outcomes: 
skills_gained: 
keywords: ["repository settings secrets", "form playbook select", "workflow run summary", "set make sure", "agent directly", "ve exported"]
---
# Setup Guide

Get the Partner Agent running locally or in GitHub Actions.

---

## Prerequisites

- Python 3.9+
- API key for Anthropic or OpenAI

---

## Local Installation

### 1. Clone the Repository

```bash
git clone https://github.com/danieloleary/PartnerOS.git
cd PartnerOS/scripts/partner_agent
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

Or install manually:

```bash
pip install anthropic pyyaml rich
# or for OpenAI
pip install openai pyyaml rich
```

### 3. Set API Key

=== "Anthropic (Recommended)"

    ```bash
    export ANTHROPIC_API_KEY=sk-ant-api03-...
    ```

=== "OpenAI"

    ```bash
    export OPENAI_API_KEY=sk-...
    ```

### 4. Run the Agent

```bash
python agent.py
```

---

## GitHub Actions Setup

Run the agent directly from GitHub's UI.

### 1. Add Secrets

Go to your repository → **Settings** → **Secrets and variables** → **Actions**

Add one or both:

| Secret Name | Value |
|-------------|-------|
| `ANTHROPIC_API_KEY` | Your Anthropic API key |
| `OPENAI_API_KEY` | Your OpenAI API key |

### 2. Run Workflow

1. Go to **Actions** tab
2. Click **Run Partner Agent** in the sidebar
3. Click **Run workflow** button
4. Fill in the form:
    - **Playbook**: Select from dropdown
    - **Partner**: Enter partner name
    - **Provider**: Choose AI provider
5. Click **Run workflow**

### 3. View Results

- Real-time logs in the workflow run
- Summary in the **Summary** tab
- Artifacts available for download

---

## Verify Installation

```bash
# Check Python version
python --version  # Should be 3.9+

# Check dependencies
pip list | grep -E "anthropic|openai|pyyaml|rich"

# Test the agent
python agent.py --status
```

Expected output:

```
No partners tracked yet.
```

---

## Troubleshooting

### "anthropic package not installed"

```bash
pip install anthropic
```

### "ANTHROPIC_API_KEY not set"

Make sure you've exported the key in your current terminal session:

```bash
export ANTHROPIC_API_KEY=sk-ant-...
# Verify
echo $ANTHROPIC_API_KEY
```

### "ModuleNotFoundError: No module named 'rich'"

Rich is optional but recommended:

```bash
pip install rich
```

### Permission Denied on agent.py

```bash
chmod +x agent.py
```

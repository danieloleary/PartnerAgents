#!/usr/bin/env python3
"""Manage PartnerAgents blueprint templates."""

import argparse
import datetime
from pathlib import Path
import re
import sys
import os
from typing import Optional

ROOT = Path("docs")

# Optional Pydantic for structured output
try:
    from pydantic import BaseModel, Field

    PYDANTIC_AVAILABLE = True

    class TemplateFrontmatter(BaseModel):
        title: str
        section: str
        category: str
        template_number: str
        version: str = "1.0.0"
        last_updated: Optional[str] = None
        author: str = "PartnerAgents Team"
        tier: str = "Bronze"
        skill_level: str = "beginner"
        purpose: str
        phase: str
        time_required: str
        difficulty: str = "medium"
        prerequisites: list[str] = Field(default_factory=list)
        outcomes: list[str] = Field(default_factory=list)
        skills_gained: list[str] = Field(default_factory=list)
        tags: list[str] = Field(default_factory=list)

    class LLMResponse(BaseModel):
        """Structured response from LLM for template generation."""

        title: str
        frontmatter: TemplateFrontmatter
        body: str

except ImportError:
    PYDANTIC_AVAILABLE = False
    TemplateFrontmatter = None
    LLMResponse = None


def parse_front_matter(lines):
    if not lines or not lines[0].startswith("---"):
        return {}, 0
    fm_lines = []
    end = 1
    for idx in range(1, len(lines)):
        line = lines[idx]
        if line.startswith("---"):
            end = idx + 1
            break
        fm_lines.append(line)
    fm = {}
    for line in fm_lines:
        if ":" in line:
            key, val = line.split(":", 1)
            fm[key.strip()] = val.strip()
    return fm, end


def format_front_matter(fm):
    lines = ["---"]
    for key, value in fm.items():
        lines.append(f"{key}: {value}")
    lines.append("---\n")
    return "\n".join(lines)


def read_file(path: Path):
    lines = path.read_text().splitlines()
    fm, start = parse_front_matter(lines)
    body = lines[start:]
    return fm, body


def write_file(path: Path, fm: dict, body: list[str]):
    content = format_front_matter(fm) + "\n".join(body)
    if not content.endswith("\n"):
        content += "\n"
    path.write_text(content)


def sanitize_title(title: str) -> str:
    return re.sub(r"[^A-Za-z0-9]+", "_", title).strip("_")


def create_template(args):
    section_dir = ROOT / args.section
    section_dir.mkdir(parents=True, exist_ok=True)
    filename = f"{args.template_number}_{sanitize_title(args.title)}.md"
    path = section_dir / filename
    if path.exists():
        print(f"Error: {path} already exists", file=sys.stderr)
        return 1
    fm = {
        "title": args.title,
        "section": args.section.replace("_", " "),
        "template_number": args.template_number,
        "last_updated": args.last_updated or str(datetime.date.today()),
        "description": ">",
        "related_templates": "",
        "keywords": "[]",
    }
    body = [
        "## How to Use This Template",
        "",
        "**Purpose:**",
        "Describe the purpose of this template.",
        "",
        "**Steps:**",
        "1. Step 1",
        "2. Step 2",
        "",
        "---",
        "",
        f"# {args.title}",
        "",
    ]
    write_file(path, fm, body)
    print(f"Created {path}")
    return 0


def update_template(args):
    path = Path(args.path)
    if not path.exists():
        print(f"Error: {path} does not exist", file=sys.stderr)
        return 1
    fm, body = read_file(path)
    for pair in args.set:
        if "=" in pair:
            k, v = pair.split("=", 1)
            fm[k.strip()] = v.strip()
    if args.last_updated:
        fm["last_updated"] = args.last_updated
    write_file(path, fm, body)
    print(f"Updated {path}")
    return 0


def revise_all(args):
    for p in ROOT.rglob("*.md"):
        fm, body = read_file(p)
        changed = False
        if args.last_updated:
            fm["last_updated"] = args.last_updated
            changed = True
        if changed:
            write_file(p, fm, body)
            print(f"Updated {p}")
    return 0


def enhance_template(args):
    path = Path(args.path)
    if not path.exists():
        print(f"Error: {path} does not exist", file=sys.stderr)
        return 1
    fm, body = read_file(path)
    try:
        from openai import OpenAI  # type: ignore
    except ImportError:
        print("openai package is required for this command", file=sys.stderr)
        return 1
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("OPENAI_API_KEY environment variable not set", file=sys.stderr)
        return 1
    client = OpenAI(api_key=api_key)

    # Build prompt with or without structured output
    if PYDANTIC_AVAILABLE and args.structured:
        # Use structured output for guaranteed parseable response
        system_prompt = """You format and enhance markdown templates. 
Output MUST be valid JSON with this exact structure:
{
  "title": "Template Title",
  "frontmatter": {
    "title": "Template Title",
    "section": "Strategy",
    "category": "strategic", 
    "template_number": "I.1",
    "version": "1.0.0",
    "last_updated": "2026-02-22",
    "author": "PartnerAgents Team",
    "tier": "Bronze",
    "skill_level": "beginner",
    "purpose": "strategic",
    "phase": "recruitment",
    "time_required": "2 hours",
    "difficulty": "medium",
    "prerequisites": [],
    "outcomes": ["Outcome 1"],
    "skills_gained": ["Skill 1"],
    "tags": ["tag1"]
  },
  "body": "The markdown body content..."
}"""
        json_schema = {
            "name": "template_response",
            "description": "Structured template response",
            "type": "object",
            "properties": {
                "title": {"type": "string"},
                "frontmatter": {
                    "type": "object",
                    "properties": {
                        "title": {"type": "string"},
                        "section": {"type": "string"},
                        "category": {"type": "string"},
                        "template_number": {"type": "string"},
                        "version": {"type": "string"},
                        "last_updated": {"type": "string"},
                        "author": {"type": "string"},
                        "tier": {"type": "string"},
                        "skill_level": {"type": "string"},
                        "purpose": {"type": "string"},
                        "phase": {"type": "string"},
                        "time_required": {"type": "string"},
                        "difficulty": {"type": "string"},
                        "prerequisites": {"type": "array", "items": {"type": "string"}},
                        "outcomes": {"type": "array", "items": {"type": "string"}},
                        "skills_gained": {"type": "array", "items": {"type": "string"}},
                        "tags": {"type": "array", "items": {"type": "string"}},
                    },
                    "required": [
                        "title",
                        "section",
                        "category",
                        "template_number",
                        "version",
                    ],
                },
                "body": {"type": "string"},
            },
            "required": ["title", "frontmatter", "body"],
        }

        try:
            resp = client.chat.completions.create(
                model=args.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": args.prompt or "\n".join(body)},
                ],
                temperature=0.3,
                response_format={"type": "json_object", "schema": json_schema},
            )
            import json

            result = json.loads(resp.choices[0].message.content)
            fm = result.get("frontmatter", fm)
            body = result.get("body", "\n".join(body)).splitlines()
        except Exception as e:
            print(
                f"Structured output failed: {e}, falling back to plain text",
                file=sys.stderr,
            )
            # Fall through to plain text mode
            resp = client.chat.completions.create(
                model=args.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You format and enhance markdown templates.",
                    },
                    {"role": "user", "content": args.prompt or "\n".join(body)},
                ],
                temperature=0.3,
            )
            improved = resp.choices[0].message.content
            body = improved.splitlines()
    else:
        # Plain text mode (original behavior)
        prompt = (
            args.prompt
            or "Clean up and format the following Markdown template:\n\n"
            + "\n".join(body)
        )
        resp = client.chat.completions.create(
            model=args.model,
            messages=[
                {
                    "role": "system",
                    "content": "You format and enhance markdown templates.",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.3,
        )
        improved = resp.choices[0].message.content
        body = improved.splitlines()

    if args.update_last_updated:
        fm["last_updated"] = str(datetime.date.today())
    write_file(path, fm, body)
    print(f"Enhanced {path}")
    return 0


def main():
    parser = argparse.ArgumentParser(description="Manage PartnerAgents blueprint templates")
    sub = parser.add_subparsers(dest="cmd")

    c = sub.add_parser("create", help="Create a new template")
    c.add_argument("section", help="Target section directory")
    c.add_argument("template_number", help="Template identifier (e.g. I.1)")
    c.add_argument("title", help="Template title")
    c.add_argument("--last-updated", dest="last_updated", help="Last updated date")
    c.set_defaults(func=create_template)

    u = sub.add_parser("update", help="Update an existing template")
    u.add_argument("path", help="Path to template file")
    u.add_argument(
        "--set", action="append", default=[], help="Frontmatter key=value pair"
    )
    u.add_argument(
        "--last-updated", dest="last_updated", help="Update last_updated field"
    )
    u.set_defaults(func=update_template)

    r = sub.add_parser("revise", help="Apply bulk revisions to all templates")
    r.add_argument(
        "--last-updated",
        dest="last_updated",
        default=str(datetime.date.today()),
        help="Set last_updated for all templates",
    )
    r.set_defaults(func=revise_all)

    e = sub.add_parser("enhance", help="Enhance a template using the OpenAI API")
    e.add_argument("path", help="Path to template file")
    e.add_argument("--model", default="gpt-3.5-turbo", help="OpenAI model ID")
    e.add_argument("--prompt", help="Optional custom prompt for the model")
    e.add_argument(
        "--update-last-updated", action="store_true", help="Set last_updated to today"
    )
    e.add_argument(
        "--structured",
        action="store_true",
        help="Use structured JSON output (requires Pydantic)",
    )
    e.set_defaults(func=enhance_template)

    args = parser.parse_args()
    if not args.cmd:
        parser.print_help()
        return 1
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())

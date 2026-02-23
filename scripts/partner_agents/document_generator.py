#!/usr/bin/env python3
"""
Document Generator - Load, fill, and save templates for PartnerOS
Handles template loading from Starlight docs and saves filled documents.
"""

import re
import os
import html
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional

# Base directory - PartnerOS root
REPO_ROOT = Path(__file__).resolve().parent.parent.parent
TEMPLATES_DIR = REPO_ROOT / "partneros-docs" / "src" / "content" / "docs"
DOCUMENTS_DIR = REPO_ROOT / "partners"


def _slugify(text: str) -> str:
    """Convert text to a URL-safe slug."""
    text = text.lower()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[-\s]+", "-", text)
    return text.strip("-")


def _ensure_partner_dir(partner_name: str) -> Path:
    """Ensure partner directory exists."""
    slug = _slugify(partner_name)
    partner_dir = DOCUMENTS_DIR / slug / "documents"
    partner_dir.mkdir(parents=True, exist_ok=True)
    return partner_dir


def extract_placeholders(content: str) -> List[str]:
    """Extract all placeholder patterns from template content."""
    placeholders = set()

    # Pattern 1: [Placeholder Name]
    bracket_pattern = r"\[([^\]]+)\]"
    for match in re.finditer(bracket_pattern, content):
        placeholders.add(match.group(1).strip())

    # Pattern 2: $variable or ${variable}
    dollar_pattern = r"\$\{?(\w+)\}?"
    for match in re.finditer(dollar_pattern, content):
        placeholders.add(match.group(1).strip())

    # Pattern 3: ___field___
    underscore_pattern = r"___([a-z_]+)___"
    for match in re.finditer(underscore_pattern, content):
        placeholders.add(match.group(1).strip())

    return list(placeholders)


def load_template(template_path: str) -> Optional[Dict[str, Any]]:
    """Load a template from the docs directory."""
    # Handle both "legal/01-nda.md" and "legal/01-nda" formats
    if not template_path.endswith(".md"):
        template_path = template_path + ".md"

    full_path = TEMPLATES_DIR / template_path

    if not full_path.exists():
        return None

    with open(full_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Parse frontmatter
    frontmatter = {}
    body = content

    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            frontmatter_text = parts[1]
            body = parts[2].strip()

            # Simple YAML parsing
            for line in frontmatter_text.split("\n"):
                if ":" in line:
                    key, value = line.split(":", 1)
                    frontmatter[key.strip()] = value.strip()

    placeholders = extract_placeholders(body)

    return {
        "path": str(full_path),
        "relative_path": template_path,
        "frontmatter": frontmatter,
        "body": body,
        "placeholders": placeholders,
    }


def fill_template(template: Dict[str, Any], fields: Dict[str, Any]) -> str:
    """Fill template with provided fields."""
    body = template["body"]

    # Pattern 1: [Placeholder Name]
    def replace_bracket(match):
        placeholder = match.group(1).strip()
        return fields.get(placeholder, match.group(0))

    body = re.sub(r"\[([^\]]+)\]", replace_bracket, body)

    # Pattern 2: $variable or ${variable}
    def replace_dollar(match):
        placeholder = match.group(1).strip()
        return fields.get(placeholder, match.group(0))

    body = re.sub(r"\$\{?(\w+)\}?", replace_dollar, body)

    # Pattern 3: ___field___
    def replace_underscore(match):
        placeholder = match.group(1).strip()
        return fields.get(placeholder, match.group(0))

    body = re.sub(r"___([a-z_]+)___", replace_underscore, body)

    return body


def save_document(partner_name: str, template_name: str, content: str) -> Path:
    """Save filled document to partner directory."""
    partner_dir = _ensure_partner_dir(partner_name)

    # Create filename with date
    date_str = datetime.now().strftime("%Y-%m-%d")
    filename = f"{date_str}-{template_name}.md"

    file_path = partner_dir / filename
    file_path.write_text(content, encoding="utf-8")

    return file_path


class DocumentGenerator:
    """Main document generator class."""

    def __init__(self):
        self.templates_dir = TEMPLATES_DIR
        self.output_dir = DOCUMENTS_DIR

    def create_document(
        self,
        doc_type: str,
        partner_name: str,
        fields: Dict[str, Any],
    ) -> Optional[Dict[str, Any]]:
        """
        Create a document for a partner.

        Args:
            doc_type: Type of document (nda, msa, dpa)
            partner_name: Name of the partner
            fields: Fields to fill in the template

        Returns:
            Dict with document info or None if failed
        """
        # Map doc type to template
        template_map = {
            "nda": "legal/01-nda.md",
            "msa": "legal/02-msa.md",
            "dpa": "legal/03-dpa.md",
        }

        template_path = template_map.get(doc_type)
        if not template_path:
            return None

        # Load template
        template = load_template(template_path)
        if not template:
            return None

        # Fill with default values + provided fields
        defaults = {
            "Partner Name": partner_name,
            "partner_name": partner_name,
            "[Partner Name]": partner_name,
            "Effective Date": datetime.now().strftime("%B %d, %Y"),
            "effective_date": datetime.now().strftime("%Y-%m-%d"),
            "Term Years": "2",
            "term_years": "2",
            "Date": datetime.now().strftime("%B %d, %Y"),
            "today_date": datetime.now().strftime("%B %d, %Y"),
        }
        defaults.update(fields)

        filled_content = fill_template(template, defaults)

        # Save document
        file_path = save_document(partner_name, doc_type, filled_content)

        return {
            "doc_type": doc_type,
            "partner_name": partner_name,
            "template": template_path,
            "path": str(file_path),
            "relative_path": str(file_path.relative_to(REPO_ROOT)),
            "fields": defaults,
            "created_at": datetime.now().isoformat(),
        }

    def get_document_path(self, partner_name: str, doc_type: str) -> Optional[Path]:
        """Get path to most recent document of a type for a partner."""
        slug = _slugify(partner_name)
        partner_dir = DOCUMENTS_DIR / slug / "documents"

        if not partner_dir.exists():
            return None

        # Find matching files
        pattern = f"*-{doc_type}.md"
        files = list(partner_dir.glob(pattern))

        if not files:
            return None

        # Return most recent
        return max(files, key=lambda f: f.stat().st_mtime)

    def list_partner_documents(self, partner_name: str) -> List[Dict[str, Any]]:
        """List all documents for a partner."""
        slug = _slugify(partner_name)
        partner_dir = DOCUMENTS_DIR / slug / "documents"

        if not partner_dir.exists():
            return []

        documents = []
        for f in sorted(
            partner_dir.glob("*.md"), key=lambda x: x.stat().st_mtime, reverse=True
        ):
            documents.append(
                {
                    "filename": f.name,
                    "path": str(f),
                    "relative_path": str(f.relative_to(REPO_ROOT)),
                    "modified": datetime.fromtimestamp(f.stat().st_mtime).isoformat(),
                }
            )

        return documents


# Convenience function
generator = DocumentGenerator()


def create_document(
    doc_type: str, partner_name: str, fields: Dict[str, Any] = None
) -> Optional[Dict[str, Any]]:
    """Quick function to create a document."""
    return generator.create_document(doc_type, partner_name, fields or {})


def list_documents(partner_name: str) -> List[Dict[str, Any]]:
    """Quick function to list partner documents."""
    return generator.list_partner_documents(partner_name)

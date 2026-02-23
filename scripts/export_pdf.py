#!/usr/bin/env python3
"""
export_pdf.py - Convert PartnerAgents markdown templates to PDF.

Requires: pip install weasyprint markdown (or uses pandoc if available)

Usage:
    python scripts/export_pdf.py                        # Export all templates
    python scripts/export_pdf.py --template strategy/01-partner-business-case.md
    python scripts/export_pdf.py --category finance     # All in a category
    python scripts/export_pdf.py --output exports/pdf/  # Custom output dir
    python scripts/export_pdf.py --list                 # List available templates
"""

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
DOCS_DIR = REPO_ROOT / "docs"
DEFAULT_OUTPUT = REPO_ROOT / "exports" / "pdf"

TEMPLATE_CATEGORIES = [
    "strategy",
    "recruitment",
    "enablement",
    "legal",
    "finance",
    "security",
    "operations",
    "executive",
    "analysis",
]

CSS = """
body {
    font-family: 'Inter', 'Helvetica Neue', Arial, sans-serif;
    font-size: 11pt;
    line-height: 1.6;
    color: #1a1a2e;
    max-width: 800px;
    margin: 0 auto;
    padding: 20px 40px;
}
h1 { font-size: 22pt; color: #1a1a2e; border-bottom: 2px solid #4f46e5; padding-bottom: 8px; }
h2 { font-size: 16pt; color: #3730a3; margin-top: 24px; }
h3 { font-size: 13pt; color: #4f46e5; }
table {
    border-collapse: collapse;
    width: 100%;
    margin: 16px 0;
    font-size: 10pt;
}
th {
    background: #4f46e5;
    color: white;
    padding: 8px 12px;
    text-align: left;
}
td { padding: 6px 12px; border-bottom: 1px solid #e5e7eb; }
tr:nth-child(even) { background: #f8fafc; }
code {
    background: #f1f5f9;
    padding: 2px 6px;
    border-radius: 3px;
    font-family: 'JetBrains Mono', 'Courier New', monospace;
    font-size: 9pt;
}
pre {
    background: #1e293b;
    color: #e2e8f0;
    padding: 16px;
    border-radius: 6px;
    overflow-x: auto;
    font-size: 9pt;
}
blockquote {
    border-left: 4px solid #4f46e5;
    margin: 16px 0;
    padding: 8px 16px;
    background: #eef2ff;
    color: #3730a3;
}
.frontmatter { display: none; }
@page {
    margin: 2cm;
    @bottom-center {
        content: "PartnerAgents — danieloleary.github.io/PartnerAgents";
        font-size: 8pt;
        color: #94a3b8;
    }
    @top-right {
        content: counter(page);
        font-size: 8pt;
        color: #94a3b8;
    }
}
"""


def find_templates(category: str = None, specific: str = None):
    """Return list of (rel_path, abs_path) tuples for templates to export."""
    templates = []
    if specific:
        p = DOCS_DIR / specific
        if not p.exists():
            print(f"Error: Template not found: {specific}", file=sys.stderr)
            sys.exit(1)
        templates.append((specific, p))
        return templates

    cats = [category] if category else TEMPLATE_CATEGORIES
    for cat in cats:
        cat_dir = DOCS_DIR / cat
        if cat_dir.exists():
            for f in sorted(cat_dir.glob("*.md")):
                if f.name not in ("index.md",):
                    rel = f.relative_to(DOCS_DIR)
                    templates.append((str(rel), f))
    return templates


def strip_frontmatter(content: str) -> str:
    """Remove YAML frontmatter block from markdown."""
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            return parts[2].strip()
    return content


def export_with_pandoc(md_path: Path, out_path: Path) -> bool:
    """Export using pandoc (preferred — better quality)."""
    cmd = [
        "pandoc",
        str(md_path),
        "-o",
        str(out_path),
        "--pdf-engine=wkhtmltopdf",
        "--variable",
        "geometry:margin=2cm",
        "--variable",
        "fontsize=11pt",
        "--variable",
        f"footer-center=PartnerAgents",
        "--variable",
        "colorlinks=true",
        "--variable",
        "linkcolor=blue",
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode == 0


def export_with_weasyprint(md_path: Path, out_path: Path) -> bool:
    """Export using weasyprint + markdown (Python-only fallback)."""
    try:
        import markdown
        from weasyprint import HTML, CSS as WeasyprintCSS
    except ImportError:
        return False

    content = md_path.read_text()
    body = strip_frontmatter(content)
    html_body = markdown.markdown(body, extensions=["tables", "fenced_code", "toc"])
    html = f"""<!DOCTYPE html>
<html>
<head><meta charset="utf-8"><style>{CSS}</style></head>
<body>{html_body}</body>
</html>"""
    HTML(string=html, base_url=str(DOCS_DIR)).write_pdf(
        str(out_path), stylesheets=[WeasyprintCSS(string=CSS)]
    )
    return True


def export_template(rel_path: str, abs_path: Path, out_dir: Path) -> str:
    """Export a single template to PDF. Returns 'ok', 'skip', or 'error'."""
    # Build output path mirroring docs/ structure
    out_path = out_dir / Path(rel_path).with_suffix(".pdf")
    out_path.parent.mkdir(parents=True, exist_ok=True)

    # Try pandoc first, then weasyprint
    if shutil.which("pandoc"):
        ok = export_with_pandoc(abs_path, out_path)
    else:
        ok = export_with_weasyprint(abs_path, out_path)

    if ok:
        return "ok"
    return "error"


def list_templates():
    """Print all exportable templates."""
    print("Available templates for PDF export:\n")
    for cat in TEMPLATE_CATEGORIES:
        cat_dir = DOCS_DIR / cat
        if cat_dir.exists():
            files = sorted(cat_dir.glob("*.md"))
            files = [f for f in files if f.name != "index.md"]
            if files:
                print(f"{cat}/")
                for f in files:
                    print(f"  {f.name}")
    print()


def main():
    parser = argparse.ArgumentParser(
        description="Export PartnerAgents templates to PDF"
    )
    parser.add_argument(
        "--template",
        "-t",
        help="Single template path relative to docs/ (e.g. strategy/01-partner-business-case.md)",
    )
    parser.add_argument(
        "--category",
        "-c",
        choices=TEMPLATE_CATEGORIES,
        help="Export all templates in a category",
    )
    parser.add_argument(
        "--output",
        "-o",
        default=str(DEFAULT_OUTPUT),
        help=f"Output directory (default: {DEFAULT_OUTPUT})",
    )
    parser.add_argument(
        "--list", "-l", action="store_true", help="List available templates"
    )
    args = parser.parse_args()

    if args.list:
        list_templates()
        return

    out_dir = Path(args.output)
    templates = find_templates(category=args.category, specific=args.template)

    if not templates:
        print("No templates found.", file=sys.stderr)
        sys.exit(1)

    # Check for PDF export capability
    has_pandoc = bool(shutil.which("pandoc"))
    try:
        import weasyprint  # noqa: F401

        has_weasyprint = True
    except ImportError:
        has_weasyprint = False

    if not has_pandoc and not has_weasyprint:
        print(
            "PDF export requires either:\n"
            "  pandoc: https://pandoc.org/installing.html\n"
            "  weasyprint: pip install weasyprint markdown\n",
            file=sys.stderr,
        )
        sys.exit(1)

    engine = "pandoc" if has_pandoc else "weasyprint"
    print(f"Exporting {len(templates)} template(s) using {engine} → {out_dir}/\n")

    ok_count = error_count = 0
    for rel_path, abs_path in templates:
        result = export_template(rel_path, abs_path, out_dir)
        out_file = out_dir / Path(rel_path).with_suffix(".pdf")
        if result == "ok":
            print(f"  ✓  {rel_path}")
            ok_count += 1
        else:
            print(f"  ✗  {rel_path}  (export failed — check tool installation)")
            error_count += 1

    print(f"\nDone: {ok_count} exported, {error_count} failed")
    if ok_count > 0:
        print(f"PDFs saved to: {out_dir}/")


if __name__ == "__main__":
    main()

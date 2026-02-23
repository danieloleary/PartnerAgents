#!/usr/bin/env python3
"""
Docling Document Processor for PartnerAgents

Parses partner documents (PDFs, DOCX, PPTX) into structured Markdown/JSON.
Part of the PartnerAgents document processing toolkit.

Usage:
    python parse_document.py --input contract.pdf --output contract.md
    python parse_document.py --input proposal.docx --output proposal.json --format json

Requirements:
    pip install docling

    # Optional: for better PDF rendering
    pip install docling[ocr]
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Optional

try:
    from docling.datamodel.base_models import InputFormat
    from docling.datamodel.pipeline_options import PdfPipelineOptions
    from docling.document_converter import DocumentConverter, PdfFormatOption
    from docling.backend.pypdf_backend import PyPdfDocumentBackend
except ImportError:
    print("ERROR: Docling not installed.")
    print("Install with: pip install docling")
    print("Or with OCR support: pip install docling[ocr]")
    sys.exit(1)


def parse_document(
    input_path: str,
    output_path: Optional[str] = None,
    format: str = "markdown",
) -> dict:
    """
    Parse a document using Docling.

    Args:
        input_path: Path to input document (PDF, DOCX, PPTX, HTML)
        output_path: Path for output file (optional)
        format: Output format - 'markdown' or 'json'

    Returns:
        Dictionary with parsed content and metadata
    """
    input_file = Path(input_path)

    if not input_file.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    print(f"📄 Parsing: {input_file.name}")

    # Configure pipeline
    pipeline_options = PdfPipelineOptions()
    pipeline_options.do_ocr = True
    pipeline_options.do_table_structure = True

    format_options = {
        InputFormat.PDF: PdfFormatOption(
            pipeline_options=pipeline_options,
            backend=PyPdfDocumentBackend,
        ),
    }

    converter = DocumentConverter(
        format_options=format_options,
    )

    # Convert document
    result = converter.convert(input_file)

    # Extract content
    if format == "markdown":
        content = result.document.export_to_markdown()
    elif format == "json":
        content = result.document.export_to_dict()
    else:
        raise ValueError(f"Unsupported format: {format}. Use 'markdown' or 'json'")

    # Build output
    output = {
        "filename": input_file.name,
        "format": format,
        "content": content,
        "metadata": {
            "page_count": len(result.document.pages)
            if hasattr(result.document, "pages")
            else 0,
        },
    }

    # Save to file if output path provided
    if output_path:
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)

        if format == "markdown":
            output_file.write_text(content, encoding="utf-8")
        else:
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(
                    json.loads(content) if isinstance(content, str) else content,
                    f,
                    indent=2,
                )

        print(f"✅ Saved to: {output_file}")

    print(f"✅ Parsed {output['metadata']['page_count']} pages")

    return output


def main():
    parser = argparse.ArgumentParser(
        description="Parse partner documents with Docling (PDF, DOCX, PPTX, HTML)"
    )
    parser.add_argument("--input", "-i", required=True, help="Input document path")
    parser.add_argument("--output", "-o", help="Output file path (optional)")
    parser.add_argument(
        "--format",
        "-f",
        choices=["markdown", "json"],
        default="markdown",
        help="Output format (default: markdown)",
    )
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")

    args = parser.parse_args()

    try:
        result = parse_document(
            input_path=args.input,
            output_path=args.output,
            format=args.format,
        )

        if not args.output:
            print("\n--- Content Preview ---")
            print(
                result["content"][:500] + "..."
                if len(result["content"]) > 500
                else result["content"]
            )

        return 0

    except Exception as e:
        print(f"❌ Error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())

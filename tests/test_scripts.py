"""Test utility scripts functionality."""

import os
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts"))


def test_fill_template_import():
    """Test fill_template.py can be imported."""
    import subprocess

    result = subprocess.run(
        ["python3", str(REPO_ROOT / "scripts" / "fill_template.py"), "--help"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert "Fill template" in result.stdout


def test_fill_template_missing_file():
    """Test fill_template handles missing file."""
    import subprocess

    result = subprocess.run(
        [
            "python3",
            str(REPO_ROOT / "scripts" / "fill_template.py"),
            "--template",
            "nonexistent.md",
        ],
        capture_output=True,
        text=True,
    )
    # Should show error message but might return 0, check output
    assert "not found" in result.stdout.lower() or result.returncode != 0


def test_fill_template_preview():
    """Test fill_template preview mode."""
    import subprocess

    # Use a real template
    template_path = REPO_ROOT / "docs" / "recruitment" / "01-email-sequence.md"
    if template_path.exists():
        result = subprocess.run(
            [
                "python3",
                str(REPO_ROOT / "scripts" / "fill_template.py"),
                "--template",
                str(template_path),
                "--preview",
            ],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0


def test_generate_report_import():
    """Test generate_report.py can be imported."""
    import subprocess

    result = subprocess.run(
        ["python3", str(REPO_ROOT / "scripts" / "generate_report.py"), "--help"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0


def test_generate_file_list_import():
    """Test generate_file_list.py can be imported."""
    import subprocess

    result = subprocess.run(
        ["python3", str(REPO_ROOT / "scripts" / "generate_file_list.py")],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert "markdown files" in result.stdout


def test_update_keywords_import():
    """Test update_keywords.py can be imported."""
    import subprocess

    result = subprocess.run(
        ["python3", str(REPO_ROOT / "scripts" / "update_keywords.py"), "--help"],
        capture_output=True,
        text=True,
    )
    # May not have --help, check if it runs
    assert result.returncode == 0


def test_lint_markdown_import():
    """Test lint_markdown.py can be imported."""
    import subprocess

    result = subprocess.run(
        ["python3", str(REPO_ROOT / "scripts" / "lint_markdown.py")],
        capture_output=True,
        text=True,
    )
    # Should run without crashing (lint errors don't count as failure)
    assert "lint errors found" in result.stdout or "pass linting" in result.stdout


def test_manage_templates_import():
    """Test manage_templates.py can be imported."""
    import subprocess

    result = subprocess.run(
        ["python3", str(REPO_ROOT / "scripts" / "manage_templates.py"), "--help"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert "Manage PartnerOS" in result.stdout


def test_manage_templates_subcommands():
    """Test manage_templates has expected subcommands."""
    import subprocess

    result = subprocess.run(
        ["python3", str(REPO_ROOT / "scripts" / "manage_templates.py"), "--help"],
        capture_output=True,
        text=True,
    )
    assert "create" in result.stdout
    assert "update" in result.stdout
    assert "revise" in result.stdout
    assert "enhance" in result.stdout


def test_generate_pptx_import():
    """Test generate_pptx.py can be imported."""
    import subprocess

    result = subprocess.run(
        ["python3", str(REPO_ROOT / "scripts" / "generate_pptx.py"), "--help"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0 or "generate" in result.stdout.lower()


def test_generate_pptx_demo_data_exists():
    """Test demo data file exists for PPTX generation."""
    demo_data_path = REPO_ROOT / "examples" / "demo-company" / "board-deck-data.json"
    assert demo_data_path.exists(), "Demo data file should exist for board deck"


def test_generate_pptx_output():
    """Test generate_pptx.py creates output file."""
    import subprocess
    import os

    # Run the generator
    result = subprocess.run(
        ["python3", str(REPO_ROOT / "scripts" / "generate_pptx.py")],
        capture_output=True,
        text=True,
    )

    # Check output file was created
    pptx_path = (
        REPO_ROOT / "partneros-docs" / "public" / "assets" / "pptx" / "board-deck.pptx"
    )
    assert pptx_path.exists(), f"PPTX file should be created at {pptx_path}"
    assert pptx_path.stat().st_size > 0, "PPTX file should not be empty"

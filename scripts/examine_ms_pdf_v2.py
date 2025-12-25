#!/usr/bin/env python3
"""Examine multiple Mississippi Extension stumpage price PDFs to understand their structure."""

import pdfplumber
from rich.console import Console
from pathlib import Path

console = Console()

# Examine multiple PDFs to see if format changes
pdf_files = [
    "ms_timber_2013_q1.pdf",
    "ms_timber_2015_q1.pdf",
    "ms_timber_2020_q1.pdf",
    "ms_timber_2025_q3.pdf"
]

base_path = Path("/Users/mihiarc/landuse-model/forest-rents/data/raw/ms_extension")

for pdf_file in pdf_files:
    pdf_path = base_path / pdf_file
    if not pdf_path.exists():
        console.print(f"[red]File not found: {pdf_file}[/red]")
        continue

    console.print(f"\n[bold cyan]{'='*80}[/bold cyan]")
    console.print(f"[bold cyan]Examining: {pdf_file}[/bold cyan]")
    console.print(f"[bold cyan]{'='*80}[/bold cyan]\n")

    with pdfplumber.open(pdf_path) as pdf:
        console.print(f"[bold]Pages:[/bold] {len(pdf.pages)}")

        # Check all pages for tables and text patterns
        for page_num, page in enumerate(pdf.pages):
            text = page.extract_text()

            console.print(f"\n[bold yellow]Page {page_num + 1}:[/bold yellow]")

            # Look for price information in text
            if text:
                lines = text.split('\n')
                for i, line in enumerate(lines):
                    # Look for lines with dollar signs or price-related keywords
                    if '$' in line or 'ton' in line.lower() or 'price' in line.lower():
                        console.print(f"  Line {i}: {line[:100]}")

                    # Look for species/product mentions
                    if any(keyword in line.lower() for keyword in ['pine', 'hardwood', 'pulpwood', 'sawtimber', 'cns']):
                        if '$' in line or 'price' in line.lower():
                            console.print(f"  [green]Product line {i}: {line[:100]}[/green]")

            # Check for tables
            tables = page.extract_tables()
            if tables:
                console.print(f"\n  [bold]Tables found: {len(tables)}[/bold]")
                for t_idx, table in enumerate(tables):
                    if table and len(table) > 0:
                        console.print(f"\n  Table {t_idx + 1}: {len(table)} rows x {len(table[0])} cols")
                        # Show first few rows
                        for row in table[:5]:
                            console.print(f"    {row}")

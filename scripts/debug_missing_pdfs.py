#!/usr/bin/env python3
"""Debug script to examine PDFs that failed to parse."""

import pdfplumber
from rich.console import Console
from pathlib import Path

console = Console()

# Check some problem files
problem_files = [
    "ms_timber_2013_q3.pdf",
    "ms_timber_2014_q1.pdf",
    "ms_timber_2018_q2.pdf",
    "ms_timber_2019_q1.pdf",
    "ms_timber_2024_q3.pdf"
]

base_path = Path("/Users/mihiarc/landuse-model/forest-rents/data/raw/ms_extension")

for pdf_file in problem_files:
    pdf_path = base_path / pdf_file
    if not pdf_path.exists():
        continue

    console.print(f"\n[bold cyan]{'='*80}[/bold cyan]")
    console.print(f"[bold cyan]{pdf_file}[/bold cyan]")
    console.print(f"[bold cyan]{'='*80}[/bold cyan]\n")

    with pdfplumber.open(pdf_path) as pdf:
        console.print(f"Pages: {len(pdf.pages)}")

        for page_num, page in enumerate(pdf.pages):
            text = page.extract_text()
            console.print(f"\n[yellow]Page {page_num + 1}:[/yellow]")

            if text:
                lines = text.split('\n')
                # Show lines with price information
                for i, line in enumerate(lines):
                    if any(keyword in line.lower() for keyword in ['price', '$', 'pine', 'hardwood', 'ton', 'quarter']):
                        console.print(f"{i:3d}: {line[:120]}")

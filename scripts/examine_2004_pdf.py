#!/usr/bin/env python3
"""
Examine the 2004 PDF structure in detail.
"""

import pdfplumber
from pathlib import Path
from rich.console import Console

console = Console()

pdf_path = Path("/Users/mihiarc/landuse-model/forest-rents/data/raw/texas_am/bimonthly_JanFeb2004.pdf")

with pdfplumber.open(pdf_path) as pdf:
    console.print(f"[bold]Total pages: {len(pdf.pages)}[/bold]\n")

    # Look at pages 1-5 for data tables
    for i in range(min(5, len(pdf.pages))):
        page = pdf.pages[i]
        console.print(f"[bold cyan]Page {i+1}:[/bold cyan]")

        text = page.extract_text()
        if text:
            lines = text.split('\n')
            console.print(f"Total lines: {len(lines)}\n")

            # Look for "Stumpage" or "Price" keywords
            for j, line in enumerate(lines):
                if 'stumpage' in line.lower() or 'price' in line.lower() or 'pine' in line.lower():
                    console.print(f"Line {j}: {line}")

        console.print("\n" + "-"*80 + "\n")

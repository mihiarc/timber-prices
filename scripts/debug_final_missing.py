#!/usr/bin/env python3
"""Debug the final missing PDFs."""

import pdfplumber
from rich.console import Console

console = Console()

files = [
    "/Users/mihiarc/landuse-model/forest-rents/data/raw/ms_extension/ms_timber_2021_q3.pdf",
    "/Users/mihiarc/landuse-model/forest-rents/data/raw/ms_extension/ms_timber_2024_q3.pdf"
]

for pdf_path in files:
    console.print(f"\n[bold cyan]{'='*80}[/bold cyan]")
    console.print(f"[bold cyan]{pdf_path}[/bold cyan]")
    console.print(f"[bold cyan]{'='*80}[/bold cyan]\n")

    with pdfplumber.open(pdf_path) as pdf:
        console.print(f"Pages: {len(pdf.pages)}")

        for page_num, page in enumerate(pdf.pages[:3]):
            text = page.extract_text()
            console.print(f"\n[yellow]Page {page_num + 1} (first 2000 chars):[/yellow]")
            console.print(text[:2000] if text else "No text")

#!/usr/bin/env python3
"""Examine the historical 1971-2001 PDF."""

import pdfplumber
from pathlib import Path
from rich.console import Console

console = Console()

pdf_path = Path("/Users/mihiarc/landuse-model/forest-rents/data/raw/oh_osu/pdfs/1971-2001.pdf")

console.print(f"[bold]Examining: {pdf_path.name}[/bold]")
console.print(f"File size: {pdf_path.stat().st_size / (1024*1024):.2f} MB\n")

with pdfplumber.open(pdf_path) as pdf:
    console.print(f"Total pages: {len(pdf.pages)}\n")

    # Sample a few pages
    for page_num in [0, 1, 2, len(pdf.pages)//2, -1]:
        if page_num < 0:
            page_num = len(pdf.pages) + page_num

        page = pdf.pages[page_num]
        console.print(f"[bold cyan]Page {page_num + 1}[/bold cyan]")
        console.print("-" * 80)

        # Extract text
        text = page.extract_text()
        if text:
            console.print("[yellow]Text content (first 500 chars):[/yellow]")
            console.print(text[:500])
        else:
            console.print("[red]No text found on this page[/red]")

        # Check for tables
        tables = page.extract_tables()
        console.print(f"\n[yellow]Number of tables: {len(tables)}[/yellow]")

        if tables:
            console.print("[green]First table preview:[/green]")
            for i, row in enumerate(tables[0][:5]):
                console.print(f"Row {i}: {row}")

        console.print("\n" + "=" * 80 + "\n")

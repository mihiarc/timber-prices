#!/usr/bin/env python3
"""Examine Ohio PDF structure to understand table format."""

import pdfplumber
from pathlib import Path
from rich.console import Console

console = Console()

pdf_path = Path("/Users/mihiarc/landuse-model/forest-rents/data/raw/oh_osu/pdfs/2024_Q1.pdf")

console.print(f"[bold]Examining: {pdf_path.name}[/bold]\n")

with pdfplumber.open(pdf_path) as pdf:
    console.print(f"Total pages: {len(pdf.pages)}\n")

    for page_num, page in enumerate(pdf.pages, 1):
        console.print(f"[bold cyan]Page {page_num}[/bold cyan]")
        console.print("-" * 80)

        # Extract text
        text = page.extract_text()
        console.print("[yellow]Text content:[/yellow]")
        console.print(text[:1500] if text else "No text found")
        console.print()

        # Extract tables
        tables = page.extract_tables()
        console.print(f"[yellow]Number of tables: {len(tables)}[/yellow]")

        for i, table in enumerate(tables, 1):
            console.print(f"\n[green]Table {i}:[/green]")
            console.print(f"Rows: {len(table)}, Columns: {len(table[0]) if table else 0}")

            # Print first few rows
            for j, row in enumerate(table[:10]):
                console.print(f"Row {j}: {row}")

        console.print("\n" + "=" * 80 + "\n")

        # Only examine first 3 pages
        if page_num >= 3:
            break

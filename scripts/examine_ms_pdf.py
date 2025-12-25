#!/usr/bin/env python3
"""Examine a Mississippi Extension stumpage price PDF to understand its structure."""

import pdfplumber
from rich.console import Console
from rich.table import Table
from rich import print as rprint

console = Console()

# Examine a sample PDF
pdf_path = "/Users/mihiarc/landuse-model/forest-rents/data/raw/ms_extension/ms_timber_2013_q1.pdf"

console.print(f"\n[bold cyan]Examining PDF:[/bold cyan] {pdf_path}\n")

with pdfplumber.open(pdf_path) as pdf:
    console.print(f"[bold]Number of pages:[/bold] {len(pdf.pages)}\n")

    # Examine first few pages
    for page_num in range(min(3, len(pdf.pages))):
        page = pdf.pages[page_num]
        console.print(f"[bold yellow]Page {page_num + 1}:[/bold yellow]")
        console.print(f"Page dimensions: {page.width} x {page.height}")

        # Extract text
        text = page.extract_text()
        console.print("\n[bold]Text content:[/bold]")
        console.print(text[:1000] if text else "No text found")
        console.print("\n" + "="*80 + "\n")

        # Extract tables
        tables = page.extract_tables()
        console.print(f"[bold]Number of tables found:[/bold] {len(tables)}\n")

        for table_idx, table in enumerate(tables):
            console.print(f"[bold green]Table {table_idx + 1}:[/bold green]")
            console.print(f"Rows: {len(table)}, Columns: {len(table[0]) if table else 0}")

            # Display table
            if table:
                rich_table = Table(show_header=True, header_style="bold magenta")

                # Add columns
                for col_idx in range(len(table[0])):
                    rich_table.add_column(f"Col {col_idx}", overflow="fold")

                # Add rows (limit to first 10)
                for row in table[:10]:
                    rich_table.add_row(*[str(cell) if cell else "" for cell in row])

                console.print(rich_table)
            console.print("\n")

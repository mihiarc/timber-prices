#!/usr/bin/env python3
"""
Examine the structure of Georgia DOR timber values PDF files.
This script helps understand the table layout before writing the full parser.
"""

import pdfplumber
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich import print as rprint

console = Console()

def examine_pdf(pdf_path: Path):
    """Examine the structure of a GA DOR timber values PDF."""

    console.print(f"\n[bold cyan]Examining PDF:[/bold cyan] {pdf_path.name}")
    console.print("=" * 80)

    with pdfplumber.open(pdf_path) as pdf:
        console.print(f"[yellow]Total pages:[/yellow] {len(pdf.pages)}")

        # Examine first few pages
        for page_num, page in enumerate(pdf.pages[:3], 1):
            console.print(f"\n[bold green]Page {page_num}:[/bold green]")
            console.print(f"  Size: {page.width} x {page.height}")

            # Extract text
            text = page.extract_text()
            if text:
                console.print(f"\n[bold]Text content (first 500 chars):[/bold]")
                console.print(text[:500])

            # Try to extract tables
            tables = page.extract_tables()
            console.print(f"\n[yellow]Number of tables found:[/yellow] {len(tables)}")

            if tables:
                for table_num, table in enumerate(tables, 1):
                    console.print(f"\n[bold magenta]Table {table_num}:[/bold magenta]")
                    console.print(f"  Rows: {len(table)}")
                    console.print(f"  Columns: {len(table[0]) if table else 0}")

                    # Display first few rows
                    console.print("\n[bold]First 5 rows:[/bold]")
                    for row_num, row in enumerate(table[:5], 1):
                        console.print(f"  Row {row_num}: {row}")

            console.print("\n" + "-" * 80)

def main():
    """Main function to examine GA DOR PDFs."""

    data_dir = Path("/Users/mihiarc/landuse-model/forest-rents/data/raw/ga_dor")

    # Examine both PDFs
    pdf_files = sorted(data_dir.glob("ga_dor_timber_values_*.pdf"))

    for pdf_file in pdf_files:
        examine_pdf(pdf_file)

if __name__ == "__main__":
    main()

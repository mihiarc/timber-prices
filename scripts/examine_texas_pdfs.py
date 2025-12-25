#!/usr/bin/env python3
"""
Examine Texas A&M Forest Service stumpage price PDFs to understand their structure.
"""

import pdfplumber
from pathlib import Path
from rich.console import Console
from rich.table import Table

console = Console()

def examine_pdf(pdf_path: Path):
    """Examine a single PDF file and print its structure."""
    console.print(f"\n[bold cyan]{'='*80}[/bold cyan]")
    console.print(f"[bold yellow]File: {pdf_path.name}[/bold yellow]")
    console.print(f"[bold cyan]{'='*80}[/bold cyan]\n")

    try:
        with pdfplumber.open(pdf_path) as pdf:
            console.print(f"[green]Total pages: {len(pdf.pages)}[/green]\n")

            # Examine first 2 pages
            for i, page in enumerate(pdf.pages[:2]):
                console.print(f"[bold magenta]Page {i+1}:[/bold magenta]")

                # Extract text
                text = page.extract_text()
                if text:
                    lines = text.split('\n')[:20]  # First 20 lines
                    console.print("[dim]Text preview:[/dim]")
                    for line in lines:
                        console.print(f"  {line}")

                # Extract tables
                tables = page.extract_tables()
                if tables:
                    console.print(f"\n[green]Found {len(tables)} table(s) on this page[/green]")
                    for j, table in enumerate(tables[:2]):  # Show first 2 tables
                        console.print(f"\n[yellow]Table {j+1} preview (first 5 rows):[/yellow]")
                        for row_idx, row in enumerate(table[:5]):
                            console.print(f"  Row {row_idx}: {row}")

                console.print("\n" + "-"*80 + "\n")

    except Exception as e:
        console.print(f"[bold red]Error reading {pdf_path.name}: {e}[/bold red]")

def main():
    """Main function to examine all Texas A&M PDFs."""
    data_dir = Path("/Users/mihiarc/landuse-model/forest-rents/data/raw/texas_am")

    # Priority order: 5-year and annual reports first
    priority_files = [
        "5year_5-Year-Stumpage-Prices-2019-2023.pdf",
        "annual_Annual-Price-Report-2023.pdf",
        "5year_Prices202017-2021.pdf",
    ]

    # Examine priority files first
    for filename in priority_files:
        pdf_path = data_dir / filename
        if pdf_path.exists():
            examine_pdf(pdf_path)

    # Then examine bimonthly files
    console.print("\n[bold blue]Examining sample bimonthly reports...[/bold blue]")
    bimonthly_files = sorted(data_dir.glob("bimonthly_*.pdf"))
    for pdf_path in bimonthly_files[:2]:  # Just first 2 bimonthly
        examine_pdf(pdf_path)

if __name__ == "__main__":
    main()

"""
Complete workflow guide for NH stumpage data acquisition and parsing.
"""

import webbrowser
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()


def main():
    """Display workflow and help user get started."""

    console.print("\n")
    console.print(Panel.fit(
        "[bold blue]NH Stumpage Data Acquisition Workflow[/bold blue]",
        border_style="blue"
    ))

    # Check current status
    data_dir = Path("/Users/mihiarc/landuse-model/forest-rents/data/raw/nh_dra")
    pdf_dir = data_dir / "pdfs"
    pdf_dir.mkdir(parents=True, exist_ok=True)

    pdf_files = list(pdf_dir.glob("*.pdf"))

    # Create status table
    status_table = Table(title="Current Status", show_header=True, header_style="bold magenta")
    status_table.add_column("Item", style="cyan")
    status_table.add_column("Status", style="green")

    status_table.add_row("Data directory", "[green]Created[/green]" if data_dir.exists() else "[red]Missing[/red]")
    status_table.add_row("PDF directory", "[green]Created[/green]" if pdf_dir.exists() else "[red]Missing[/red]")
    status_table.add_row("PDFs downloaded", f"[cyan]{len(pdf_files)} files[/cyan]")

    console.print("\n")
    console.print(status_table)
    console.print("\n")

    if pdf_files:
        console.print("[bold green]Found PDFs:[/bold green]")
        for pdf in pdf_files:
            console.print(f"  [cyan]✓[/cyan] {pdf.name}")
        console.print("\n")
        console.print("[bold green]Ready to parse![/bold green]")
        console.print("Run: [cyan]uv run python scripts/parse_nh_stumpage.py[/cyan]\n")

    else:
        console.print("[bold yellow]No PDFs found - Manual download required[/bold yellow]\n")

        # Show the problem
        console.print(Panel(
            "[yellow]The NH DRA website uses Akamai bot protection that blocks all automated downloads.\n"
            "All HTTP libraries (requests, httpx, urllib, curl, wget) return 403 Forbidden.\n"
            "Therefore, PDFs must be downloaded manually through a web browser.[/yellow]",
            title="Why Manual Download?",
            border_style="yellow"
        ))

        console.print("\n[bold]Download Instructions:[/bold]\n")

        # Create step table
        steps = Table(show_header=False, box=None)
        steps.add_column("Step", style="bold cyan", width=8)
        steps.add_column("Action")

        steps.add_row(
            "STEP 1",
            "Visit: [link]https://www.revenue.nh.gov/taxes-glance/timber-tax/average-stumpage-value-information[/link]"
        )
        steps.add_row(
            "STEP 2",
            "Click on PDF links to download reports (look for 'avg-stump-val-*.pdf')"
        )
        steps.add_row(
            "STEP 3",
            f"Save PDFs to: [cyan]{pdf_dir}[/cyan]"
        )
        steps.add_row(
            "STEP 4",
            "Run parser: [green]uv run python scripts/parse_nh_stumpage.py[/green]"
        )

        console.print(steps)

        # Show recommended PDFs to download
        console.print("\n[bold]Recommended PDFs to Download (2021-2025):[/bold]\n")

        pdf_table = Table(show_header=True, header_style="bold blue")
        pdf_table.add_column("Period", style="cyan")
        pdf_table.add_column("Filename", style="yellow")

        pdf_recommendations = [
            ("Oct 2024 - Mar 2025", "avg-stump-val-10-24-03-25.pdf"),
            ("Apr 2024 - Sep 2024", "avg-stump-val-04-24-09-24.pdf"),
            ("Oct 2023 - Mar 2024", "avg-stump-val-10-23-03-24.pdf"),
            ("Apr 2023 - Sep 2023", "avg-stump-val-04-23-09-23.pdf"),
            ("Oct 2022 - Mar 2023", "avg-stump-val-10-22-03-23.pdf"),
            ("Apr 2022 - Sep 2022", "avg-stump-val-04-22-09-22.pdf"),
            ("Oct 2021 - Mar 2022", "avg-stump-val-10-21-03-22.pdf"),
            ("Apr 2021 - Sep 2021", "avg-stump-val-04-21-09-21.pdf"),
        ]

        for period, filename in pdf_recommendations:
            pdf_table.add_row(period, filename)

        console.print(pdf_table)

        # Ask if user wants to open browser
        console.print("\n")
        response = console.input("[bold]Open download page in browser now? (y/n):[/bold] ")

        if response.lower().strip() in ['y', 'yes']:
            url = "https://www.revenue.nh.gov/taxes-glance/timber-tax/average-stumpage-value-information"
            console.print(f"\n[green]Opening {url}[/green]\n")
            webbrowser.open(url)
            console.print("[cyan]After downloading PDFs, run this script again to check status.[/cyan]\n")
        else:
            console.print("\n[cyan]No problem! Download PDFs manually when ready.[/cyan]\n")

    # Show what the output will look like
    console.print(Panel(
        "[bold]Expected Output Format:[/bold]\n\n"
        "CSV columns: year, period, period_dates, region, species, product_type, price_low, price_high, unit\n"
        "Example: 2024, Fall, 10/2024-03/2025, Northern, White Pine, Sawlogs, 250.00, 350.00, MBF\n\n"
        "The parser extracts pricing data for all regions (Northern, Central, Southern)\n"
        "and all species/products from each PDF report.",
        title="Output Format",
        border_style="green"
    ))

    console.print("\n[bold blue]For more details, see:[/bold blue] [cyan]MANUAL_DOWNLOAD_GUIDE.md[/cyan]\n")


if __name__ == "__main__":
    main()

"""
Open the NH DRA stumpage value page in the default browser for manual download.
"""

import webbrowser
from rich.console import Console

console = Console()

URL = "https://www.revenue.nh.gov/taxes-glance/timber-tax/average-stumpage-value-information"

console.print("\n[bold blue]Opening NH DRA Stumpage Value Page[/bold blue]\n")
console.print("The website will open in your default browser.")
console.print("\n[bold]Instructions:[/bold]")
console.print("1. Download the desired PDF reports from the page")
console.print("2. Save them to: [cyan]data/raw/nh_dra/pdfs/[/cyan]")
console.print("3. Run: [green]uv run python scripts/parse_nh_stumpage.py[/green]")
console.print("\n[yellow]Note:[/yellow] Look for files named like:")
console.print("  - avg-stump-val-10-24-03-25.pdf")
console.print("  - avg-stump-val-04-24-09-24.pdf")
console.print("  - etc.\n")

# Open URL in browser
webbrowser.open(URL)

console.print("[green]Browser opened![/green] Please download the PDFs and save them to the pdfs/ directory.\n")

#!/usr/bin/env python3
"""
Validate the parsed GA DOR timber values data.
"""

import pandas as pd
from pathlib import Path
from rich.console import Console
from rich.table import Table as RichTable
from rich import print as rprint

console = Console()


def main():
    """Validate the parsed data."""

    csv_path = Path("/Users/mihiarc/landuse-model/forest-rents/data/raw/ga_dor/ga_stumpage_parsed.csv")

    console.print("\n[bold cyan]GA DOR Timber Values - Data Validation[/bold cyan]")
    console.print("=" * 80)

    # Load data
    df = pd.read_csv(csv_path)

    console.print(f"\n[bold]Total records:[/bold] {len(df):,}")
    console.print(f"[bold]File size:[/bold] {csv_path.stat().st_size:,} bytes")

    # Check for missing values
    console.print("\n[bold yellow]Missing values:[/bold yellow]")
    missing = df.isnull().sum()
    for col, count in missing.items():
        if count > 0:
            console.print(f"  {col}: {count}")
        else:
            console.print(f"  {col}: [green]✓ No missing values[/green]")

    # Check data types
    console.print("\n[bold yellow]Data types:[/bold yellow]")
    for col, dtype in df.dtypes.items():
        console.print(f"  {col}: {dtype}")

    # Summary statistics for prices
    console.print("\n[bold yellow]Price statistics ($/ton):[/bold yellow]")
    price_stats = df["price_avg"].describe()
    console.print(f"  Count: {price_stats['count']:.0f}")
    console.print(f"  Mean:  ${price_stats['mean']:.2f}")
    console.print(f"  Std:   ${price_stats['std']:.2f}")
    console.print(f"  Min:   ${price_stats['min']:.2f}")
    console.print(f"  25%:   ${price_stats['25%']:.2f}")
    console.print(f"  50%:   ${price_stats['50%']:.2f}")
    console.print(f"  75%:   ${price_stats['75%']:.2f}")
    console.print(f"  Max:   ${price_stats['max']:.2f}")

    # Records per year
    console.print("\n[bold yellow]Records per year:[/bold yellow]")
    year_counts = df["year"].value_counts().sort_index()
    for year, count in year_counts.items():
        console.print(f"  {year}: {count:,} records")

    # Counties per year
    console.print("\n[bold yellow]Counties per year:[/bold yellow]")
    for year in sorted(df["year"].unique()):
        county_count = df[df["year"] == year]["county"].nunique()
        console.print(f"  {year}: {county_count} counties")

    # Product types and species
    console.print("\n[bold yellow]Product types:[/bold yellow]")
    for species in sorted(df["species"].unique()):
        products = df[df["species"] == species]["product_type"].unique()
        console.print(f"  {species}: {', '.join(sorted(products))}")

    # Sample counties with highest and lowest average prices
    console.print("\n[bold green]Counties with highest average stumpage prices (2025):[/bold green]")
    df_2025 = df[df["year"] == 2025]
    top_counties = df_2025.groupby("county")["price_avg"].mean().sort_values(ascending=False).head(5)

    table = RichTable(show_header=True, header_style="bold magenta")
    table.add_column("Rank", style="cyan", justify="right")
    table.add_column("County", style="green")
    table.add_column("Avg Price", justify="right", style="white")

    for rank, (county, price) in enumerate(top_counties.items(), 1):
        table.add_row(str(rank), county, f"${price:.2f}")

    console.print(table)

    console.print("\n[bold green]Counties with lowest average stumpage prices (2025):[/bold green]")
    bottom_counties = df_2025.groupby("county")["price_avg"].mean().sort_values().head(5)

    table = RichTable(show_header=True, header_style="bold magenta")
    table.add_column("Rank", style="cyan", justify="right")
    table.add_column("County", style="green")
    table.add_column("Avg Price", justify="right", style="white")

    for rank, (county, price) in enumerate(bottom_counties.items(), 1):
        table.add_row(str(rank), county, f"${price:.2f}")

    console.print(table)

    # Price comparison by product type (2024 vs 2025)
    console.print("\n[bold green]Average price changes by product type (2024 → 2025):[/bold green]")

    comparison = df.groupby(["year", "species", "product_type"])["price_avg"].mean().unstack(level=0)

    if 2024 in comparison.columns and 2025 in comparison.columns:
        comparison["change"] = comparison[2025] - comparison[2024]
        comparison["pct_change"] = (comparison["change"] / comparison[2024]) * 100

        table = RichTable(show_header=True, header_style="bold magenta")
        table.add_column("Species", style="yellow")
        table.add_column("Product Type", style="blue")
        table.add_column("2024", justify="right", style="cyan")
        table.add_column("2025", justify="right", style="cyan")
        table.add_column("Change", justify="right", style="white")
        table.add_column("% Change", justify="right", style="white")

        for (species, product), row in comparison.iterrows():
            change_color = "green" if row["change"] >= 0 else "red"
            table.add_row(
                species,
                product,
                f"${row[2024]:.2f}",
                f"${row[2025]:.2f}",
                f"[{change_color}]${row['change']:+.2f}[/{change_color}]",
                f"[{change_color}]{row['pct_change']:+.1f}%[/{change_color}]"
            )

        console.print(table)

    console.print("\n[bold cyan]=" * 40)
    console.print("[bold green]✓ Validation complete![/bold green]")
    console.print("[bold cyan]=" * 40 + "\n")


if __name__ == "__main__":
    main()

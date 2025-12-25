"""
Analyze and visualize Tennessee stumpage price data.
Run after parsing PDFs to explore trends and patterns.
"""
import pandas as pd
from pathlib import Path
from rich.console import Console
from rich.table import Table
import warnings
warnings.filterwarnings('ignore')

console = Console()


def load_data(csv_path: Path) -> pd.DataFrame:
    """Load stumpage price data."""
    if not csv_path.exists():
        console.print(f"[red]Error: Data file not found: {csv_path}[/red]")
        console.print("[yellow]Run parse_tn_bulletins.py first to generate data[/yellow]")
        return None

    df = pd.read_csv(csv_path)
    console.print(f"[green]Loaded {len(df)} records from {csv_path.name}[/green]\n")
    return df


def data_summary(df: pd.DataFrame) -> None:
    """Display comprehensive data summary."""
    console.print("[bold cyan]Data Summary[/bold cyan]\n")

    summary_table = Table(show_header=True, header_style="bold magenta")
    summary_table.add_column("Metric", style="cyan", width=30)
    summary_table.add_column("Value", style="green")

    summary_table.add_row("Total Records", f"{len(df):,}")
    summary_table.add_row("Date Range", f"{df['year'].min()}-{df['year'].max()}")
    summary_table.add_row("Years Covered", f"{df['year'].nunique()}")
    summary_table.add_row("Quarters Covered", f"{len(df.groupby(['year', 'quarter']))}")
    summary_table.add_row("Unique Species", f"{df['species'].nunique()}")
    summary_table.add_row("Unique Regions", f"{df['region'].nunique()}")
    summary_table.add_row("Product Types", f"{df['product_type'].nunique()}")
    summary_table.add_row("Units", f"{df['unit'].nunique()}")

    # Missing data
    missing = df.isnull().sum().sum()
    summary_table.add_row("Missing Values", f"{missing}")

    # Price ranges
    if 'price_avg' in df.columns:
        summary_table.add_row("Price Range (avg)",
                             f"${df['price_avg'].min():.2f} - ${df['price_avg'].max():.2f}")

    console.print(summary_table)


def coverage_analysis(df: pd.DataFrame) -> None:
    """Analyze temporal coverage and gaps."""
    console.print("\n[bold cyan]Coverage Analysis[/bold cyan]\n")

    # Expected vs actual quarters
    year_range = range(df['year'].min(), df['year'].max() + 1)
    expected_quarters = len(year_range) * 4
    actual_quarters = len(df.groupby(['year', 'quarter']))

    coverage_pct = (actual_quarters / expected_quarters) * 100

    console.print(f"Expected quarters: {expected_quarters}")
    console.print(f"Actual quarters: {actual_quarters}")
    console.print(f"Coverage: {coverage_pct:.1f}%\n")

    # Find missing quarters
    all_quarters = [(y, q) for y in year_range for q in range(1, 5)]
    actual_quarters_set = set(df.groupby(['year', 'quarter']).groups.keys())
    missing_quarters = [q for q in all_quarters if q not in actual_quarters_set]

    if missing_quarters:
        console.print(f"[yellow]Missing {len(missing_quarters)} quarters:[/yellow]")
        # Show first 20
        for year, quarter in missing_quarters[:20]:
            console.print(f"  {year} Q{quarter}")
        if len(missing_quarters) > 20:
            console.print(f"  ... and {len(missing_quarters) - 20} more")
    else:
        console.print("[green]No missing quarters - complete coverage![/green]")


def species_breakdown(df: pd.DataFrame) -> None:
    """Show breakdown by species."""
    console.print("\n[bold cyan]Species Breakdown[/bold cyan]\n")

    species_counts = df['species'].value_counts().head(15)

    species_table = Table(show_header=True, header_style="bold magenta")
    species_table.add_column("Species", style="cyan")
    species_table.add_column("Records", justify="right", style="green")
    species_table.add_column("% of Total", justify="right", style="yellow")

    for species, count in species_counts.items():
        pct = (count / len(df)) * 100
        species_table.add_row(species, f"{count:,}", f"{pct:.1f}%")

    console.print(species_table)


def product_type_breakdown(df: pd.DataFrame) -> None:
    """Show breakdown by product type."""
    console.print("\n[bold cyan]Product Type Breakdown[/bold cyan]\n")

    product_counts = df['product_type'].value_counts()

    product_table = Table(show_header=True, header_style="bold magenta")
    product_table.add_column("Product Type", style="cyan")
    product_table.add_column("Records", justify="right", style="green")
    product_table.add_column("Unit", style="yellow")

    for product_type, count in product_counts.items():
        # Get most common unit for this product type
        common_unit = df[df['product_type'] == product_type]['unit'].mode()
        unit = common_unit.iloc[0] if len(common_unit) > 0 else 'unknown'
        product_table.add_row(product_type, f"{count:,}", unit)

    console.print(product_table)


def regional_breakdown(df: pd.DataFrame) -> None:
    """Show breakdown by region."""
    console.print("\n[bold cyan]Regional Breakdown[/bold cyan]\n")

    region_counts = df['region'].value_counts()

    region_table = Table(show_header=True, header_style="bold magenta")
    region_table.add_column("Region", style="cyan")
    region_table.add_column("Records", justify="right", style="green")

    for region, count in region_counts.items():
        region_table.add_row(region, f"{count:,}")

    console.print(region_table)


def price_trends(df: pd.DataFrame) -> None:
    """Show price trends for major species/product combinations."""
    console.print("\n[bold cyan]Price Trends - Pine Sawtimber (Statewide)[/bold cyan]\n")

    # Filter for pine sawtimber statewide
    pine_saw = df[
        (df['species'].str.contains('Pine', case=False, na=False)) &
        (df['product_type'] == 'sawtimber') &
        (df['region'] == 'statewide')
    ].copy()

    if len(pine_saw) == 0:
        console.print("[yellow]No pine sawtimber data found[/yellow]")
        return

    # Create year-quarter column for sorting
    pine_saw['yq'] = pine_saw['year'].astype(str) + ' Q' + pine_saw['quarter'].astype(str)
    pine_saw = pine_saw.sort_values(['year', 'quarter'])

    # Show last 20 quarters
    recent = pine_saw.tail(20)

    trend_table = Table(show_header=True, header_style="bold magenta")
    trend_table.add_column("Period", style="cyan")
    trend_table.add_column("Avg Price", justify="right", style="green")
    trend_table.add_column("Range", justify="right", style="yellow")
    trend_table.add_column("Unit", style="blue")

    for _, row in recent.iterrows():
        period = f"{int(row['year'])} Q{int(row['quarter'])}"
        avg_price = f"${row['price_avg']:.2f}" if pd.notna(row['price_avg']) else 'N/A'

        if pd.notna(row['price_low']) and pd.notna(row['price_high']):
            price_range = f"${row['price_low']:.2f} - ${row['price_high']:.2f}"
        else:
            price_range = 'N/A'

        trend_table.add_row(period, avg_price, price_range, str(row['unit']))

    console.print(trend_table)

    # Calculate growth rate
    if len(pine_saw) >= 2:
        first_price = pine_saw.iloc[0]['price_avg']
        last_price = pine_saw.iloc[-1]['price_avg']

        if pd.notna(first_price) and pd.notna(last_price) and first_price > 0:
            total_growth = ((last_price - first_price) / first_price) * 100
            years_span = pine_saw.iloc[-1]['year'] - pine_saw.iloc[0]['year']

            console.print(f"\n[bold]Price Change:[/bold]")
            console.print(f"  First: ${first_price:.2f} ({int(pine_saw.iloc[0]['year'])} Q{int(pine_saw.iloc[0]['quarter'])})")
            console.print(f"  Last:  ${last_price:.2f} ({int(pine_saw.iloc[-1]['year'])} Q{int(pine_saw.iloc[-1]['quarter'])})")
            console.print(f"  Total: {total_growth:+.1f}% over {years_span} years")

            if years_span > 0:
                annual_growth = total_growth / years_span
                console.print(f"  Annual: {annual_growth:+.1f}% per year")


def price_statistics(df: pd.DataFrame) -> None:
    """Show price statistics by product type."""
    console.print("\n[bold cyan]Price Statistics by Product Type[/bold cyan]\n")

    stats_table = Table(show_header=True, header_style="bold magenta")
    stats_table.add_column("Product Type", style="cyan")
    stats_table.add_column("Unit", style="blue")
    stats_table.add_column("Mean", justify="right", style="green")
    stats_table.add_column("Median", justify="right", style="yellow")
    stats_table.add_column("Min", justify="right", style="red")
    stats_table.add_column("Max", justify="right", style="green")

    for product_type in df['product_type'].unique():
        product_data = df[df['product_type'] == product_type]

        if 'price_avg' in product_data.columns:
            prices = product_data['price_avg'].dropna()

            if len(prices) > 0:
                common_unit = product_data['unit'].mode()
                unit = common_unit.iloc[0] if len(common_unit) > 0 else 'unknown'

                stats_table.add_row(
                    product_type,
                    unit,
                    f"${prices.mean():.2f}",
                    f"${prices.median():.2f}",
                    f"${prices.min():.2f}",
                    f"${prices.max():.2f}"
                )

    console.print(stats_table)


def main():
    """Main analysis function."""
    console.print("\n[bold cyan]Tennessee Stumpage Price Data Analysis[/bold cyan]\n")

    # Try both possible CSV locations
    csv_paths = [
        Path("/Users/mihiarc/landuse-model/forest-rents/data/raw/tn_forestry/tn_stumpage_parsed.csv"),
        Path("/Users/mihiarc/landuse-model/forest-rents/data/raw/tn_forestry/tn_stumpage_SAMPLE.csv"),
    ]

    df = None
    for csv_path in csv_paths:
        if csv_path.exists():
            df = load_data(csv_path)
            break

    if df is None:
        console.print("[red]No data file found![/red]")
        console.print("\n[yellow]Expected locations:[/yellow]")
        for path in csv_paths:
            console.print(f"  {path}")
        return

    # Run all analyses
    data_summary(df)
    coverage_analysis(df)
    species_breakdown(df)
    product_type_breakdown(df)
    regional_breakdown(df)
    price_trends(df)
    price_statistics(df)

    console.print("\n[bold green]Analysis complete![/bold green]\n")


if __name__ == "__main__":
    main()

"""
Demo script showing how the TN Bulletin parser would work with sample data.
Creates a sample CSV showing expected output format.
"""
import pandas as pd
from pathlib import Path
from rich.console import Console
from rich.table import Table

console = Console()


def create_sample_data():
    """Create sample stumpage price data matching expected format."""

    # Sample data representing what would be extracted from PDFs
    sample_records = [
        # Q1 2017 - Pine Sawtimber
        {
            'year': 2017, 'quarter': 1, 'region': 'statewide',
            'species': 'Pine', 'product_type': 'sawtimber',
            'price_avg': 285.50, 'price_low': 250.00, 'price_high': 320.00,
            'unit': 'MBF'
        },
        {
            'year': 2017, 'quarter': 1, 'region': 'east',
            'species': 'Pine', 'product_type': 'sawtimber',
            'price_avg': 295.00, 'price_low': 270.00, 'price_high': 320.00,
            'unit': 'MBF'
        },
        {
            'year': 2017, 'quarter': 1, 'region': 'west',
            'species': 'Pine', 'product_type': 'sawtimber',
            'price_avg': 275.00, 'price_low': 250.00, 'price_high': 300.00,
            'unit': 'MBF'
        },

        # Q1 2017 - Pine Pulpwood
        {
            'year': 2017, 'quarter': 1, 'region': 'statewide',
            'species': 'Pine', 'product_type': 'pulpwood',
            'price_avg': 8.50, 'price_low': 7.00, 'price_high': 10.00,
            'unit': 'ton'
        },

        # Q1 2017 - Hardwood Sawtimber
        {
            'year': 2017, 'quarter': 1, 'region': 'statewide',
            'species': 'White Oak', 'product_type': 'sawtimber',
            'price_avg': 425.00, 'price_low': 350.00, 'price_high': 500.00,
            'unit': 'MBF'
        },
        {
            'year': 2017, 'quarter': 1, 'region': 'statewide',
            'species': 'Red Oak', 'product_type': 'sawtimber',
            'price_avg': 375.00, 'price_low': 300.00, 'price_high': 450.00,
            'unit': 'MBF'
        },
        {
            'year': 2017, 'quarter': 1, 'region': 'statewide',
            'species': 'Yellow Poplar', 'product_type': 'sawtimber',
            'price_avg': 350.00, 'price_low': 275.00, 'price_high': 425.00,
            'unit': 'MBF'
        },

        # Q1 2017 - Hardwood Pulpwood
        {
            'year': 2017, 'quarter': 1, 'region': 'statewide',
            'species': 'Mixed Hardwood', 'product_type': 'pulpwood',
            'price_avg': 6.75, 'price_low': 5.50, 'price_high': 8.00,
            'unit': 'ton'
        },

        # Q4 2016 - Pine Sawtimber
        {
            'year': 2016, 'quarter': 4, 'region': 'statewide',
            'species': 'Pine', 'product_type': 'sawtimber',
            'price_avg': 280.00, 'price_low': 245.00, 'price_high': 315.00,
            'unit': 'MBF'
        },

        # Q4 2016 - Pine Pulpwood
        {
            'year': 2016, 'quarter': 4, 'region': 'statewide',
            'species': 'Pine', 'product_type': 'pulpwood',
            'price_avg': 8.25, 'price_low': 6.75, 'price_high': 9.75,
            'unit': 'ton'
        },

        # Earlier years - showing historical trend
        {
            'year': 2015, 'quarter': 1, 'region': 'statewide',
            'species': 'Pine', 'product_type': 'sawtimber',
            'price_avg': 265.00, 'price_low': 230.00, 'price_high': 300.00,
            'unit': 'MBF'
        },
        {
            'year': 2014, 'quarter': 1, 'region': 'statewide',
            'species': 'Pine', 'product_type': 'sawtimber',
            'price_avg': 255.00, 'price_low': 220.00, 'price_high': 290.00,
            'unit': 'MBF'
        },
        {
            'year': 2013, 'quarter': 1, 'region': 'statewide',
            'species': 'Pine', 'product_type': 'sawtimber',
            'price_avg': 245.00, 'price_low': 210.00, 'price_high': 280.00,
            'unit': 'MBF'
        },

        # Historical data points
        {
            'year': 2000, 'quarter': 1, 'region': 'statewide',
            'species': 'Pine', 'product_type': 'sawtimber',
            'price_avg': 215.00, 'price_low': 180.00, 'price_high': 250.00,
            'unit': 'MBF'
        },
        {
            'year': 1990, 'quarter': 1, 'region': 'statewide',
            'species': 'Pine', 'product_type': 'sawtimber',
            'price_avg': 175.00, 'price_low': 140.00, 'price_high': 210.00,
            'unit': 'MBF'
        },
        {
            'year': 1980, 'quarter': 1, 'region': 'statewide',
            'species': 'Pine', 'product_type': 'sawtimber',
            'price_avg': 125.00, 'price_low': 100.00, 'price_high': 150.00,
            'unit': 'MBF'
        },
    ]

    return sample_records


def main():
    """Create and display sample output."""
    console.print("\n[bold cyan]Tennessee Stumpage Price Data - Sample Output[/bold cyan]\n")
    console.print("[yellow]Note: This is SAMPLE data showing expected format.[/yellow]")
    console.print("[yellow]Actual data will be extracted from downloaded PDFs.[/yellow]\n")

    # Create sample data
    sample_data = create_sample_data()
    df = pd.DataFrame(sample_data)

    # Sort by year, quarter
    df = df.sort_values(['year', 'quarter', 'region', 'species'])

    # Save to CSV
    output_dir = Path("/Users/mihiarc/landuse-model/forest-rents/data/raw/tn_forestry")
    output_dir.mkdir(parents=True, exist_ok=True)

    sample_csv = output_dir / "tn_stumpage_SAMPLE.csv"
    df.to_csv(sample_csv, index=False)

    console.print(f"[green]Sample CSV created: {sample_csv}[/green]\n")

    # Display summary
    summary_table = Table(title="Sample Data Summary")
    summary_table.add_column("Metric", style="cyan")
    summary_table.add_column("Value", style="green")

    summary_table.add_row("Total records", str(len(df)))
    summary_table.add_row("Years covered", f"{df['year'].min()}-{df['year'].max()}")
    summary_table.add_row("Unique species", str(df['species'].nunique()))
    summary_table.add_row("Unique regions", str(df['region'].nunique()))
    summary_table.add_row("Unique product types", str(df['product_type'].nunique()))

    console.print(summary_table)

    # Display sample records
    console.print("\n[bold]Sample Records:[/bold]")
    sample_display = df.head(10)

    data_table = Table(show_header=True, header_style="bold magenta")
    for col in df.columns:
        data_table.add_column(col)

    for _, row in sample_display.iterrows():
        data_table.add_row(*[str(val) for val in row])

    console.print(data_table)

    # Show price trend for Pine Sawtimber
    console.print("\n[bold]Pine Sawtimber Price Trend (Statewide Average):[/bold]")
    pine_sawtimber = df[
        (df['species'] == 'Pine') &
        (df['product_type'] == 'sawtimber') &
        (df['region'] == 'statewide')
    ].sort_values('year')

    trend_table = Table(show_header=True)
    trend_table.add_column("Year", style="cyan")
    trend_table.add_column("Quarter", style="cyan")
    trend_table.add_column("Price Avg", style="green", justify="right")
    trend_table.add_column("Price Range", style="yellow", justify="right")

    for _, row in pine_sawtimber.iterrows():
        price_range = f"${row['price_low']:.2f} - ${row['price_high']:.2f}"
        trend_table.add_row(
            str(row['year']),
            f"Q{row['quarter']}",
            f"${row['price_avg']:.2f}",
            price_range
        )

    console.print(trend_table)

    # Instructions
    console.print("\n[bold cyan]Next Steps:[/bold cyan]")
    console.print("1. Download actual PDFs to: /Users/mihiarc/landuse-model/forest-rents/data/raw/tn_forestry/")
    console.print("2. Run: uv run python src/parse_tn_bulletins.py")
    console.print("3. Output will be saved to: tn_stumpage_parsed.csv")
    console.print("\n[bold]See docs/TN_BULLETIN_DOWNLOAD_GUIDE.md for download instructions[/bold]")


if __name__ == "__main__":
    main()

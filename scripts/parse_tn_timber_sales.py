"""Parse Tennessee State Forest timber sale data for stumpage prices.

The Tennessee Division of Forestry publishes timber sale results with
winning bid amounts and volumes, from which stumpage prices can be calculated.

Data source:
- https://www.tn.gov/agriculture/forests/state-forests/timber-sale-archive.html

Output: data/raw/tn_forestry/tn_state_forest_sales.csv
"""

import pandas as pd
from pathlib import Path
from rich.console import Console
from rich.table import Table

console = Console()

# Paths
RAW_DIR = Path("data/raw/tn_forestry")

# Tennessee State Forest timber sale data (extracted from web archive)
# Volume is in board feet (Doyle Rule), prices in dollars
# FY runs July 1 - June 30, so FY 2023 = calendar 2023, FY 2024 = calendar 2024, etc.

TIMBER_SALES = [
    # FY 2025 Hardwood
    {"fy": 2025, "sale": "A-04-25-01", "forest": "Chuck Swan", "type": "hardwood", "volume_bf": 892446, "bid": 375700.75},
    {"fy": 2025, "sale": "A-03-25-01", "forest": "Chickasaw", "type": "hardwood", "volume_bf": 343400, "bid": 79355.00},
    {"fy": 2025, "sale": "A-10-25-01", "forest": "Pickett", "type": "hardwood", "volume_bf": 250573, "bid": 35500.00},
    {"fy": 2025, "sale": "A-04-25-02", "forest": "Chuck Swan", "type": "hardwood", "volume_bf": 420568, "bid": 133730.80},
    {"fy": 2025, "sale": "A-04-25-03", "forest": "Chuck Swan", "type": "hardwood", "volume_bf": 671168, "bid": 159711.20},
    {"fy": 2025, "sale": "A-13-25-01", "forest": "Standing Stone", "type": "hardwood", "volume_bf": 424747, "bid": 190198.10},
    {"fy": 2025, "sale": "A-11-25-01", "forest": "Prentice Cooper", "type": "hardwood", "volume_bf": 618976, "bid": 125000.00},
    {"fy": 2025, "sale": "A-05-25-01", "forest": "Franklin", "type": "hardwood", "volume_bf": 297700, "bid": 70718.00},
    {"fy": 2025, "sale": "A-09-25-04", "forest": "Natchez Trace", "type": "hardwood", "volume_bf": 243672, "bid": 218888.00},
    {"fy": 2025, "sale": "A-09-25-05", "forest": "Natchez Trace", "type": "hardwood", "volume_bf": 352033, "bid": 245107.59},
    {"fy": 2025, "sale": "A-09-25-06", "forest": "Natchez Trace", "type": "hardwood", "volume_bf": 345622, "bid": 393479.11},
    {"fy": 2025, "sale": "A-09-25-07", "forest": "Natchez Trace", "type": "hardwood", "volume_bf": 400309, "bid": 348888.00},
    {"fy": 2025, "sale": "A-08-25-01", "forest": "Lone Mountain", "type": "hardwood", "volume_bf": 395994, "bid": 142762.00},

    # FY 2025 Pine
    {"fy": 2025, "sale": "A-03-25-02", "forest": "Chickasaw", "type": "pine", "volume_bf": 480700, "bid": 102177.00},
    {"fy": 2025, "sale": "A-03-25-03", "forest": "Chickasaw", "type": "pine", "volume_bf": 473500, "bid": 49630.00},
    {"fy": 2025, "sale": "A-09-25-01", "forest": "Natchez Trace", "type": "pine", "volume_bf": 243053, "bid": 41580.00},
    {"fy": 2025, "sale": "A-09-25-02", "forest": "Natchez Trace", "type": "pine", "volume_bf": 443566, "bid": 90440.00},
    {"fy": 2025, "sale": "A-07-25-01", "forest": "Lewis", "type": "pine", "volume_bf": 2045472, "bid": 277777.00},

    # FY 2025 Mixed
    {"fy": 2025, "sale": "A-03-25-04", "forest": "Chickasaw", "type": "mixed", "volume_bf": 376600, "bid": 75000.00},
    {"fy": 2025, "sale": "A-03-25-05", "forest": "Chickasaw", "type": "mixed", "volume_bf": 526000, "bid": 143409.82},
    {"fy": 2025, "sale": "A-09-25-03", "forest": "Natchez Trace", "type": "mixed", "volume_bf": 251767, "bid": 45660.00},

    # FY 2024 Hardwood
    {"fy": 2024, "sale": "A-04-24-02", "forest": "Chuck Swan", "type": "hardwood", "volume_bf": 360763, "bid": 57294.22},
    {"fy": 2024, "sale": "A-08-24-01", "forest": "Lone Mountain", "type": "hardwood", "volume_bf": 692387, "bid": 243679.00},
    {"fy": 2024, "sale": "A-04-24-03", "forest": "Chuck Swan", "type": "hardwood", "volume_bf": 357862, "bid": 66623.20},
    {"fy": 2024, "sale": "A-09-24-01", "forest": "Natchez Trace", "type": "hardwood", "volume_bf": 344800, "bid": 123900.00},
    {"fy": 2024, "sale": "A-09-24-03", "forest": "Natchez Trace", "type": "hardwood", "volume_bf": 332100, "bid": 378288.00},
    {"fy": 2024, "sale": "A-11-24-01", "forest": "Prentice Cooper", "type": "hardwood", "volume_bf": 793119, "bid": 167151.52},
    {"fy": 2024, "sale": "A-13-24-01", "forest": "Standing Stone", "type": "hardwood", "volume_bf": 381453, "bid": 211623.00},
    {"fy": 2024, "sale": "A-09-24-04", "forest": "Natchez Trace", "type": "hardwood", "volume_bf": 307600, "bid": 454888.00},
    {"fy": 2024, "sale": "A-09-24-05", "forest": "Natchez Trace", "type": "hardwood", "volume_bf": 372200, "bid": 399987.70},
    {"fy": 2024, "sale": "A-09-24-02", "forest": "Natchez Trace", "type": "hardwood", "volume_bf": 271800, "bid": 370888.00},
    {"fy": 2024, "sale": "A-04-24-04", "forest": "Chuck Swan", "type": "hardwood", "volume_bf": 202365, "bid": 66779.60},
    {"fy": 2024, "sale": "A-04-24-05", "forest": "Chuck Swan", "type": "hardwood", "volume_bf": 567684, "bid": 175860.05},
    {"fy": 2024, "sale": "A-05-24-01", "forest": "Franklin", "type": "hardwood", "volume_bf": 691800, "bid": 340895.06},

    # FY 2024 Pine
    {"fy": 2024, "sale": "A-09-24-06", "forest": "Natchez Trace", "type": "pine", "volume_bf": 426800, "bid": 132850.00},
    {"fy": 2024, "sale": "A-09-24-07", "forest": "Natchez Trace", "type": "pine", "volume_bf": 311400, "bid": 82650.00},

    # FY 2024 Mixed
    {"fy": 2024, "sale": "A-09-24-08", "forest": "Natchez Trace", "type": "mixed", "volume_bf": 361300, "bid": 142900.00},

    # FY 2023 Hardwood
    {"fy": 2023, "sale": "A-04-23-01", "forest": "Chuck Swan", "type": "hardwood", "volume_bf": 331379, "bid": 88331.00},
    {"fy": 2023, "sale": "A-13-23-01", "forest": "Standing Stone", "type": "hardwood", "volume_bf": 195590, "bid": 151562.00},
    {"fy": 2023, "sale": "A-09-23-01", "forest": "Natchez Trace", "type": "hardwood", "volume_bf": 278596, "bid": 281546.00},
    {"fy": 2023, "sale": "A-09-23-02", "forest": "Natchez Trace", "type": "hardwood", "volume_bf": 270954, "bid": 228898.00},
    {"fy": 2023, "sale": "A-09-23-03", "forest": "Natchez Trace", "type": "hardwood", "volume_bf": 434329, "bid": 289916.44},
    {"fy": 2023, "sale": "A-09-23-04", "forest": "Natchez Trace", "type": "hardwood", "volume_bf": 520418, "bid": 241348.57},
    {"fy": 2023, "sale": "A-09-23-05", "forest": "Natchez Trace", "type": "hardwood", "volume_bf": 409061, "bid": 110261.09},
    {"fy": 2023, "sale": "A-11-23-01", "forest": "Prentice Cooper", "type": "hardwood", "volume_bf": 532959, "bid": 82593.00},
    {"fy": 2023, "sale": "A-05-23-01", "forest": "Franklin", "type": "hardwood", "volume_bf": 485886, "bid": 195347.70},

    # FY 2023 Pine
    {"fy": 2023, "sale": "A-09-23-06", "forest": "Natchez Trace", "type": "pine", "volume_bf": 703480, "bid": 151160.00},
    {"fy": 2023, "sale": "A-09-23-07", "forest": "Natchez Trace", "type": "pine", "volume_bf": 442207, "bid": 67999.00},
    {"fy": 2023, "sale": "A-09-23-08", "forest": "Natchez Trace", "type": "pine", "volume_bf": 536831, "bid": 121266.00},
]


def calculate_prices() -> pd.DataFrame:
    """Calculate stumpage prices from timber sale data."""
    rows = []

    for sale in TIMBER_SALES:
        volume_mbf = sale['volume_bf'] / 1000  # Convert BF to MBF
        price_per_mbf = (sale['bid'] / volume_mbf) if volume_mbf > 0 else 0

        rows.append({
            'fiscal_year': sale['fy'],
            'calendar_year': sale['fy'],  # FY roughly aligns with calendar year
            'sale_id': sale['sale'],
            'state_forest': sale['forest'],
            'timber_type': sale['type'],
            'volume_mbf': round(volume_mbf, 2),
            'winning_bid': sale['bid'],
            'price_per_mbf': round(price_per_mbf, 2),
        })

    return pd.DataFrame(rows)


def aggregate_by_year_type(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate prices by year and timber type."""
    agg = df.groupby(['calendar_year', 'timber_type']).agg({
        'price_per_mbf': ['mean', 'min', 'max', 'count'],
        'volume_mbf': 'sum',
        'winning_bid': 'sum',
    }).round(2)

    agg.columns = ['price_avg', 'price_low', 'price_high', 'num_sales', 'total_volume', 'total_value']
    agg = agg.reset_index()

    return agg


def main():
    console.print("[bold]Parsing Tennessee State Forest Timber Sales[/bold]\n")

    # Calculate prices from sales data
    df = calculate_prices()

    console.print(f"[blue]Processed {len(df)} timber sales[/blue]")

    # Show raw sales summary
    table = Table(title="TN Timber Sales Summary")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="green")
    table.add_row("Total sales", str(len(df)))
    table.add_row("Fiscal years", f"{df['fiscal_year'].min()} - {df['fiscal_year'].max()}")
    table.add_row("Total volume (MBF)", f"{df['volume_mbf'].sum():,.0f}")
    table.add_row("Total value", f"${df['winning_bid'].sum():,.0f}")
    console.print(table)

    # Ensure output directory exists
    RAW_DIR.mkdir(parents=True, exist_ok=True)

    # Save raw sales data
    raw_path = RAW_DIR / "tn_state_forest_sales.csv"
    df.to_csv(raw_path, index=False)
    console.print(f"\n[green]Saved raw sales to {raw_path}[/green]")

    # Aggregate by year and type
    agg = aggregate_by_year_type(df)

    # Save aggregated data
    agg_path = RAW_DIR / "tn_stumpage_parsed.csv"
    agg.to_csv(agg_path, index=False)
    console.print(f"[green]Saved aggregated prices to {agg_path}[/green]")

    # Show price summary
    console.print("\n[bold]Stumpage Prices by Year and Type:[/bold]")
    console.print(agg.to_string(index=False))

    # Show by timber type
    console.print("\n[bold]Average Prices by Timber Type:[/bold]")
    type_avg = df.groupby('timber_type')['price_per_mbf'].agg(['mean', 'min', 'max', 'count']).round(2)
    type_avg.columns = ['avg_$/MBF', 'min_$/MBF', 'max_$/MBF', 'sales']
    console.print(type_avg.to_string())

    # Show by state forest
    console.print("\n[bold]Prices by State Forest:[/bold]")
    forest_avg = df.groupby('state_forest')['price_per_mbf'].agg(['mean', 'count']).round(2)
    forest_avg.columns = ['avg_$/MBF', 'sales']
    forest_avg = forest_avg.sort_values('avg_$/MBF', ascending=False)
    console.print(forest_avg.to_string())


if __name__ == "__main__":
    main()

"""Integrate Tennessee State Forest timber sale data into the unified dataset.

This adds stumpage prices calculated from actual timber sale bids and volumes
for Tennessee state forests (FY 2023-2025).

Data source:
- tn_state_forest_sales.csv from parse_tn_timber_sales.py

Output: Updates data/processed/stumpage_unified.csv
"""

import pandas as pd
from pathlib import Path
from rich.console import Console
from rich.table import Table

console = Console()

# Paths
RAW_DIR = Path("data/raw/tn_forestry")
UNIFIED_PATH = Path("data/processed/stumpage_unified.csv")

# MBF to tons conversion (hardwood ~5 tons/MBF, softwood ~4 tons/MBF)
MBF_TO_TONS_HARDWOOD = 5.0
MBF_TO_TONS_SOFTWOOD = 4.0


def load_tn_sales() -> pd.DataFrame:
    """Load the parsed TN timber sales data."""
    path = RAW_DIR / "tn_state_forest_sales.csv"
    df = pd.read_csv(path)
    console.print(f"[blue]Loaded TN sales data:[/blue] {len(df)} rows ({df['calendar_year'].min()}-{df['calendar_year'].max()})")
    return df


def transform_to_unified(df: pd.DataFrame) -> pd.DataFrame:
    """Transform TN sales data to unified schema."""
    rows = []

    # Group by year and timber type for aggregation
    agg = df.groupby(['calendar_year', 'timber_type']).agg({
        'price_per_mbf': ['mean', 'min', 'max', 'count'],
        'volume_mbf': 'sum',
        'winning_bid': 'sum',
    }).round(2)

    agg.columns = ['price_avg', 'price_low', 'price_high', 'num_sales', 'total_volume', 'total_value']
    agg = agg.reset_index()

    for _, row in agg.iterrows():
        year = int(row['calendar_year'])
        timber_type = row['timber_type']

        # Map timber type to species category
        if timber_type == 'hardwood':
            species = 'mixed_hardwood'
            mbf_to_tons = MBF_TO_TONS_HARDWOOD
        elif timber_type == 'pine':
            species = 'southern_pine'
            mbf_to_tons = MBF_TO_TONS_SOFTWOOD
        else:  # mixed
            species = 'mixed'
            mbf_to_tons = 4.5  # average

        price_avg = float(row['price_avg'])
        price_per_ton = price_avg / mbf_to_tons

        rows.append({
            'source': 'TN',
            'year': year,
            'quarter': None,
            'period_type': 'annual',
            'region': 'Tennessee',
            'county': None,
            'species': species,
            'product_type': 'sawtimber',
            'price_avg': price_avg,
            'price_low': float(row['price_low']),
            'price_high': float(row['price_high']),
            'unit': '$/MBF',
            'price_per_ton': round(price_per_ton, 2),
            'conversion_factor': mbf_to_tons,
            'sample_size': int(row['num_sales']),
            'notes': f"TN State Forest timber sales (FY {year}). Doyle Rule. Calculated from winning bids.",
        })

    return pd.DataFrame(rows)


def show_summary(df: pd.DataFrame, title: str):
    """Display summary statistics."""
    table = Table(title=title)
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="green")

    table.add_row("Total rows", str(len(df)))
    table.add_row("Year range", f"{df['year'].min()} - {df['year'].max()}")
    table.add_row("Species", str(df['species'].nunique()))

    console.print(table)


def main():
    console.print("[bold]Integrating Tennessee State Forest Stumpage Data[/bold]\n")

    # Load TN sales data
    tn_df = load_tn_sales()

    # Transform to unified schema
    console.print("\n[yellow]Transforming data...[/yellow]")
    tn_unified = transform_to_unified(tn_df)

    show_summary(tn_unified, "TN Data Transformed")

    # Load existing unified dataset
    console.print("\n[yellow]Loading existing unified dataset...[/yellow]")
    existing_df = pd.read_csv(UNIFIED_PATH)
    console.print(f"[blue]Existing rows:[/blue] {len(existing_df)}")

    # Check for existing TN data
    existing_tn = existing_df[existing_df['source'] == 'TN']
    console.print(f"[blue]Existing TN rows:[/blue] {len(existing_tn)}")

    if len(existing_tn) > 0:
        # Show existing TN year range
        console.print(f"[blue]Existing TN years:[/blue] {existing_tn['year'].min()}-{existing_tn['year'].max()}")

        # Only add new years that don't overlap
        new_years = tn_unified[~tn_unified['year'].isin(existing_tn['year'])]
        if len(new_years) > 0:
            console.print(f"[yellow]Adding {len(new_years)} new TN records for years not in existing data[/yellow]")
            tn_unified = new_years
        else:
            # Replace TN data with new aggregated data
            console.print(f"[yellow]Replacing existing TN data with new state forest data[/yellow]")
            existing_df = existing_df[existing_df['source'] != 'TN']

    # Append new data
    unified_df = pd.concat([existing_df, tn_unified], ignore_index=True)

    # Sort by source, year
    unified_df = unified_df.sort_values(['source', 'year', 'quarter'], na_position='last')

    # Save
    unified_df.to_csv(UNIFIED_PATH, index=False)
    console.print(f"\n[green]Saved unified dataset:[/green] {len(unified_df)} total rows")

    # Show final summary
    console.print("\n[bold]Integration complete![/bold]")

    # Count TN rows in final dataset
    final_tn = unified_df[unified_df['source'] == 'TN']
    console.print(f"  TN total rows: {len(final_tn)}")
    console.print(f"  TN year range: {final_tn['year'].min()}-{final_tn['year'].max()}")
    console.print(f"  Total unified: {len(unified_df)} rows")

    # Show TN price summary
    console.print("\n[bold]TN Stumpage Prices by Species:[/bold]")
    tn_summary = final_tn.groupby('species').agg({
        'year': ['min', 'max', 'count'],
        'price_avg': 'mean'
    }).round(2)
    tn_summary.columns = ['first_year', 'last_year', 'records', 'avg_price']
    console.print(tn_summary.to_string())


if __name__ == "__main__":
    main()

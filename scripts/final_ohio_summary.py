#!/usr/bin/env python3
"""Final summary of Ohio stumpage data extraction."""

import pandas as pd
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()

# Load the data
data_file = Path("/Users/mihiarc/landuse-model/forest-rents/data/raw/oh_osu/oh_stumpage_parsed.csv")
df = pd.read_csv(data_file)

# Header
console.print("\n")
console.print(Panel.fit(
    "[bold cyan]Ohio Stumpage Price Data - Extraction Complete[/bold cyan]",
    border_style="cyan"
))

# Overall statistics
console.print("\n[bold yellow]Dataset Overview:[/bold yellow]")
stats_table = Table(show_header=False, box=None)
stats_table.add_column("Metric", style="bold")
stats_table.add_column("Value")

stats_table.add_row("Output file:", str(data_file))
stats_table.add_row("Total records:", f"{len(df):,}")
stats_table.add_row("Year range:", f"{df['year'].min()}-{df['year'].max()}")
stats_table.add_row("Unique years:", str(df['year'].nunique()))
stats_table.add_row("Unique species:", str(df['species'].nunique()))
stats_table.add_row("Unique regions:", str(df['region'].nunique()))
stats_table.add_row("Data unit:", "$/MBF (Doyle Scale)")

console.print(stats_table)

# Species list
console.print("\n[bold yellow]Species Included:[/bold yellow]")
species_list = sorted(df['species'].unique())
for i, species in enumerate(species_list, 1):
    count = len(df[df['species'] == species])
    avg_price = df[df['species'] == species]['price_avg'].mean()
    console.print(f"  {i:2d}. {species:15s} - {count:4d} records, avg: ${avg_price:7.2f}/MBF")

# Regions
console.print("\n[bold yellow]Regions:[/bold yellow]")
regions = sorted(df['region'].unique())
for region in regions:
    count = len(df[df['region'] == region])
    console.print(f"  - {region:12s}: {count:4d} records")

# Year coverage
console.print("\n[bold yellow]Temporal Coverage:[/bold yellow]")
year_counts = df['year'].value_counts().sort_index()
missing_years = []
for year in range(df['year'].min(), df['year'].max() + 1):
    if year not in year_counts:
        missing_years.append(year)

if missing_years:
    console.print(f"  Missing years: {', '.join(map(str, missing_years))}")
else:
    console.print("  Complete coverage (no missing years)")

console.print(f"  Years with data: {len(year_counts)}")
console.print(f"  Total year span: {df['year'].max() - df['year'].min() + 1} years")

# Price statistics
console.print("\n[bold yellow]Price Statistics ($/MBF):[/bold yellow]")
price_stats = Table(show_header=True, header_style="bold magenta")
price_stats.add_column("Statistic")
price_stats.add_column("Value", justify="right")

price_stats.add_row("Mean", f"${df['price_avg'].mean():.2f}")
price_stats.add_row("Median", f"${df['price_avg'].median():.2f}")
price_stats.add_row("Std Dev", f"${df['price_avg'].std():.2f}")
price_stats.add_row("Min", f"${df['price_avg'].min():.2f}")
price_stats.add_row("25th percentile", f"${df['price_avg'].quantile(0.25):.2f}")
price_stats.add_row("75th percentile", f"${df['price_avg'].quantile(0.75):.2f}")
price_stats.add_row("Max", f"${df['price_avg'].max():.2f}")

console.print(price_stats)

# Most recent data sample
console.print("\n[bold yellow]Sample Recent Data (2025 Q3):[/bold yellow]")
recent_sample = df[(df['year'] == 2025) & (df['quarter'] == 'Q3')].head(12)

sample_table = Table(show_header=True, header_style="bold cyan")
sample_table.add_column("Year")
sample_table.add_column("Quarter")
sample_table.add_column("Region")
sample_table.add_column("Species")
sample_table.add_column("Avg Price", justify="right")
sample_table.add_column("Low", justify="right")
sample_table.add_column("High", justify="right")

for _, row in recent_sample.iterrows():
    sample_table.add_row(
        str(int(row['year'])),
        row['quarter'],
        row['region'],
        row['species'],
        f"${row['price_avg']:.0f}",
        f"${row['price_low']:.0f}" if pd.notna(row['price_low']) else "N/A",
        f"${row['price_high']:.0f}" if pd.notna(row['price_high']) else "N/A",
    )

console.print(sample_table)

# Success message
console.print("\n")
console.print(Panel.fit(
    "[bold green]Data extraction and parsing completed successfully![/bold green]",
    border_style="green"
))
console.print()

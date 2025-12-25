#!/usr/bin/env python3
"""
Verify and summarize the parsed Texas A&M stumpage price data.
"""

import pandas as pd
from pathlib import Path
from rich.console import Console
from rich.table import Table

console = Console()

# Load the parsed data
csv_path = Path("/Users/mihiarc/landuse-model/forest-rents/data/raw/texas_am/tx_stumpage_parsed.csv")
df = pd.read_csv(csv_path)

console.print("\n[bold blue]Texas A&M Stumpage Price Data Verification[/bold blue]\n")

# Basic info
console.print(f"[cyan]CSV file:[/cyan] {csv_path}")
console.print(f"[cyan]File size:[/cyan] {csv_path.stat().st_size:,} bytes")
console.print(f"[cyan]Total records:[/cyan] {len(df)}")
console.print(f"[cyan]Columns:[/cyan] {', '.join(df.columns)}\n")

# Data completeness
console.print("[bold yellow]Data Completeness:[/bold yellow]")
completeness = pd.DataFrame({
    'Column': df.columns,
    'Non-Null': df.count(),
    'Null': df.isna().sum(),
    'Completeness %': (df.count() / len(df) * 100).round(1)
})

table = Table(show_header=True, header_style="bold magenta")
table.add_column("Column")
table.add_column("Non-Null", justify="right")
table.add_column("Null", justify="right")
table.add_column("Completeness %", justify="right")

for _, row in completeness.iterrows():
    table.add_row(
        row['Column'],
        str(row['Non-Null']),
        str(row['Null']),
        f"{row['Completeness %']}%"
    )

console.print(table)

# Year coverage
console.print("\n[bold yellow]Year Coverage:[/bold yellow]")
year_detail = df.groupby('year').agg({
    'region': 'nunique',
    'species': 'nunique',
    'product_type_normalized': 'nunique',
    'price_avg': ['count', 'mean', 'min', 'max']
}).round(2)

year_table = Table(show_header=True, header_style="bold cyan")
year_table.add_column("Year", justify="center")
year_table.add_column("Regions", justify="right")
year_table.add_column("Species", justify="right")
year_table.add_column("Products", justify="right")
year_table.add_column("Records", justify="right")
year_table.add_column("Avg Price", justify="right")

for year in sorted(df['year'].unique()):
    year_data = df[df['year'] == year]
    year_table.add_row(
        str(year),
        str(year_data['region'].nunique()),
        str(year_data['species'].nunique()),
        str(year_data['product_type_normalized'].nunique()),
        str(len(year_data)),
        f"${year_data['price_avg'].mean():.2f}"
    )

console.print(year_table)

# Regional coverage
console.print("\n[bold yellow]Regional Coverage:[/bold yellow]")
region_summary = df.groupby('region').agg({
    'year': ['min', 'max', 'nunique'],
    'price_avg': ['count', 'mean']
}).round(2)

region_table = Table(show_header=True, header_style="bold green")
region_table.add_column("Region")
region_table.add_column("First Year", justify="center")
region_table.add_column("Last Year", justify="center")
region_table.add_column("Years", justify="right")
region_table.add_column("Records", justify="right")
region_table.add_column("Avg Price", justify="right")

for region in sorted(df['region'].unique()):
    region_data = df[df['region'] == region]
    region_table.add_row(
        region,
        str(region_data['year'].min()),
        str(region_data['year'].max()),
        str(region_data['year'].nunique()),
        str(len(region_data)),
        f"${region_data['price_avg'].mean():.2f}"
    )

console.print(region_table)

# Product type detail
console.print("\n[bold yellow]Product Type Detail:[/bold yellow]")
product_detail = df.groupby(['species', 'product_type_normalized']).agg({
    'year': ['min', 'max', 'nunique'],
    'price_avg': ['count', 'mean', 'min', 'max']
}).round(2)

product_table = Table(show_header=True, header_style="bold yellow", show_lines=True)
product_table.add_column("Species")
product_table.add_column("Product Type")
product_table.add_column("Years", justify="center")
product_table.add_column("Records", justify="right")
product_table.add_column("Avg $/ton", justify="right")
product_table.add_column("Min $/ton", justify="right")
product_table.add_column("Max $/ton", justify="right")

for (species, product) in sorted(df.groupby(['species', 'product_type_normalized']).groups.keys()):
    data = df[(df['species'] == species) & (df['product_type_normalized'] == product)]
    product_table.add_row(
        species,
        product,
        f"{data['year'].min()}-{data['year'].max()}",
        str(len(data)),
        f"${data['price_avg'].mean():.2f}",
        f"${data['price_avg'].min():.2f}",
        f"${data['price_avg'].max():.2f}"
    )

console.print(product_table)

console.print("\n[bold green]Verification complete![/bold green]\n")

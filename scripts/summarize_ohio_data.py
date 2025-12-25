#!/usr/bin/env python3
"""Generate summary statistics for Ohio stumpage data."""

import pandas as pd
from rich.console import Console
from rich.table import Table

console = Console()

# Load the data
df = pd.read_csv('/Users/mihiarc/landuse-model/forest-rents/data/raw/oh_osu/oh_stumpage_parsed.csv')

# Summary statistics
console.print('[bold cyan]Ohio Stumpage Price Data Summary[/bold cyan]\n')
console.print(f'Total records: {len(df):,}')
console.print(f'Year range: {df["year"].min()}-{df["year"].max()}')
console.print(f'Unique species: {df["species"].nunique()}')
console.print(f'Unique regions: {df["region"].nunique()}\n')

# Species breakdown
console.print('[bold]Species distribution:[/bold]')
species_table = Table(show_header=True, header_style='bold magenta')
species_table.add_column('Species')
species_table.add_column('Count', justify='right')
species_table.add_column('Avg Price ($/MBF)', justify='right')

for species in sorted(df['species'].unique()):
    count = len(df[df['species'] == species])
    avg_price = df[df['species'] == species]['price_avg'].mean()
    species_table.add_row(species, str(count), f'${avg_price:.2f}')

console.print(species_table)

# Region breakdown
console.print('\n[bold]Region distribution:[/bold]')
region_table = Table(show_header=True, header_style='bold magenta')
region_table.add_column('Region')
region_table.add_column('Count', justify='right')

for region in sorted(df['region'].unique()):
    count = len(df[df['region'] == region])
    region_table.add_row(region, str(count))

console.print(region_table)

# Year coverage
console.print('\n[bold]Records by year:[/bold]')
year_counts = df['year'].value_counts().sort_index()
for year, count in year_counts.items():
    console.print(f'{year}: {count} records')

# Sample recent data
console.print('\n[bold]Sample recent data (2025):[/bold]')
recent = df[df['year'] == 2025].head(15)
sample_table = Table(show_header=True, header_style='bold cyan')
for col in recent.columns:
    sample_table.add_column(col)

for _, row in recent.iterrows():
    sample_table.add_row(*[str(val) for val in row])

console.print(sample_table)

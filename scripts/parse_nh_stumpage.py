"""
Parse New Hampshire stumpage price data from manually downloaded PDFs.

Due to bot protection on the NH DRA website, PDFs must be manually downloaded
and placed in the data/raw/nh_dra/pdfs/ directory.

Instructions:
1. Visit https://www.revenue.nh.gov/taxes-glance/timber-tax/average-stumpage-value-information
2. Download PDF reports and save them to: data/raw/nh_dra/pdfs/
3. Run this script to parse the PDFs into CSV format
"""

import re
import time
from pathlib import Path
from typing import List, Dict, Optional
import pandas as pd
import pdfplumber
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console()


def parse_period_from_filename(filename: str) -> Optional[Dict[str, str]]:
    """Extract year and period information from PDF filename.

    Args:
        filename: PDF filename (e.g., 'avg-stump-val-10-24-03-25.pdf')

    Returns:
        Dictionary with 'start_month', 'start_year', 'end_month', 'end_year'
        or None if pattern doesn't match
    """
    # Pattern: avg-stump-val-MM-YY-MM-YY.pdf
    pattern = r'avg-stump-val-(\d{2})-(\d{2})-(\d{2})-(\d{2})\.pdf'
    match = re.match(pattern, filename)

    if match:
        start_month, start_year, end_month, end_year = match.groups()
        # Convert 2-digit year to 4-digit (20XX)
        start_year = f"20{start_year}"
        end_year = f"20{end_year}"

        return {
            'start_month': start_month,
            'start_year': start_year,
            'end_month': end_month,
            'end_year': end_year
        }
    return None


def determine_period(start_month: str) -> str:
    """Determine if the period is Spring or Fall based on start month.

    Args:
        start_month: Two-digit month string (e.g., '04' for April)

    Returns:
        'Spring' or 'Fall'
    """
    month_int = int(start_month)
    if month_int >= 4 and month_int <= 9:
        return 'Spring'
    else:
        return 'Fall'


def clean_price_value(value: str) -> Optional[float]:
    """Clean and convert price string to float.

    Args:
        value: Price string (may contain '$', commas, etc.)

    Returns:
        Float value or None if conversion fails
    """
    if not value or value.strip() == '':
        return None

    # Remove dollar signs, commas, and whitespace
    cleaned = value.replace('$', '').replace(',', '').strip()

    try:
        return float(cleaned)
    except ValueError:
        return None


def parse_stumpage_pdf(pdf_path: Path) -> List[Dict]:
    """Parse a NH stumpage value PDF and extract pricing data.

    Args:
        pdf_path: Path to the PDF file

    Returns:
        List of dictionaries containing parsed data
    """
    records = []

    # Extract period info from filename
    period_info = parse_period_from_filename(pdf_path.name)
    if not period_info:
        console.print(f"[yellow]Warning: Could not parse period from filename {pdf_path.name}[/yellow]")
        # Try to extract year from PDF content or use generic info
        period_info = {
            'start_month': '00',
            'start_year': '2024',
            'end_month': '00',
            'end_year': '2024'
        }

    # Use the start year as the primary year
    year = period_info['start_year']
    period = determine_period(period_info['start_month'])
    period_dates = f"{period_info['start_month']}/{period_info['start_year']}-{period_info['end_month']}/{period_info['end_year']}"

    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages, 1):
            # Extract text and tables
            text = page.extract_text()
            tables = page.extract_tables()

            if not text:
                continue

            # Try to identify current region from text
            current_region = None
            text_upper = text.upper()
            if 'NORTHERN' in text_upper:
                current_region = 'Northern'
            if 'CENTRAL' in text_upper:
                current_region = 'Central'
            if 'SOUTHERN' in text_upper:
                current_region = 'Southern'

            # Process each table on the page
            for table in tables:
                if not table or len(table) < 2:
                    continue

                # Look for header row to identify columns
                header_row_idx = None
                for idx, row in enumerate(table):
                    if row and any(cell and ('SPECIES' in str(cell).upper() or
                                             'PRODUCT' in str(cell).upper() or
                                             'LOW' in str(cell).upper() or
                                             'HIGH' in str(cell).upper()) for cell in row):
                        header_row_idx = idx
                        break

                if header_row_idx is None:
                    continue

                # Process data rows
                for row in table[header_row_idx + 1:]:
                    if not row or len(row) < 3:
                        continue

                    # Skip empty or header-like rows
                    if not any(row) or all(not cell or str(cell).strip() == '' for cell in row):
                        continue

                    # Common table structure: Species | Product Type | Low | High | Unit
                    # or: Species/Product | Low | High | Unit
                    species = str(row[0]).strip() if row[0] else ''

                    # Skip if this looks like a header or total row
                    if any(keyword in species.upper() for keyword in ['SPECIES', 'PRODUCT', 'AVERAGE', 'RANGE', 'NORTHERN', 'CENTRAL', 'SOUTHERN', 'TYPE']):
                        continue

                    if not species:
                        continue

                    # Try to extract product type, low, high, unit
                    # Table layouts vary, so we need to be flexible
                    product_type = ''
                    price_low = None
                    price_high = None
                    unit = ''

                    if len(row) >= 5:
                        # Format: Species | Product | Low | High | Unit
                        product_type = str(row[1]).strip() if row[1] else ''
                        price_low = clean_price_value(str(row[2])) if row[2] else None
                        price_high = clean_price_value(str(row[3])) if row[3] else None
                        unit = str(row[4]).strip() if row[4] else ''
                    elif len(row) >= 4:
                        # Format: Species/Product | Low | High | Unit
                        price_low = clean_price_value(str(row[1])) if row[1] else None
                        price_high = clean_price_value(str(row[2])) if row[2] else None
                        unit = str(row[3]).strip() if row[3] else ''
                    elif len(row) >= 3:
                        # Format: Species | Low | High
                        price_low = clean_price_value(str(row[1])) if row[1] else None
                        price_high = clean_price_value(str(row[2])) if row[2] else None

                    # Skip if we don't have valid price data
                    if price_low is None and price_high is None:
                        continue

                    record = {
                        'year': year,
                        'period': period,
                        'period_dates': period_dates,
                        'region': current_region if current_region else 'Unknown',
                        'species': species,
                        'product_type': product_type,
                        'price_low': price_low,
                        'price_high': price_high,
                        'unit': unit
                    }
                    records.append(record)

    return records


def main():
    """Main execution function."""
    console.print("\n[bold blue]NH Stumpage Data Parser[/bold blue]\n")

    # Setup directories
    data_dir = Path("/Users/mihiarc/landuse-model/forest-rents/data/raw/nh_dra")
    data_dir.mkdir(parents=True, exist_ok=True)

    pdf_dir = data_dir / "pdfs"
    pdf_dir.mkdir(exist_ok=True)

    # Find all PDFs in the directory
    pdf_files = list(pdf_dir.glob("*.pdf"))

    if not pdf_files:
        console.print("[red]No PDF files found in data/raw/nh_dra/pdfs/[/red]")
        console.print("\n[yellow]Please manually download PDFs from:[/yellow]")
        console.print("https://www.revenue.nh.gov/taxes-glance/timber-tax/average-stumpage-value-information")
        console.print(f"\n[yellow]And save them to:[/yellow] {pdf_dir}")
        return

    console.print(f"[green]Found {len(pdf_files)} PDF file(s)[/green]")
    for pdf in pdf_files:
        console.print(f"  - {pdf.name}")

    # Parse PDFs
    console.print("\n[bold]Parsing PDFs[/bold]")
    all_records = []

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        task = progress.add_task("Parsing PDFs...", total=len(pdf_files))

        for pdf_path in pdf_files:
            console.print(f"[cyan]Parsing:[/cyan] {pdf_path.name}")
            records = parse_stumpage_pdf(pdf_path)
            all_records.extend(records)
            console.print(f"[green]Extracted {len(records)} records[/green]")
            progress.advance(task)

    # Convert to DataFrame
    if not all_records:
        console.print("[red]No records extracted from PDFs[/red]")
        return

    df = pd.DataFrame(all_records)

    # Reorder columns
    column_order = ['year', 'period', 'period_dates', 'region', 'species',
                    'product_type', 'price_low', 'price_high', 'unit']
    df = df[column_order]

    # Sort by year and period
    df = df.sort_values(['year', 'period', 'region', 'species'])

    # Save to CSV
    output_csv = data_dir / "nh_stumpage_parsed.csv"
    df.to_csv(output_csv, index=False)
    console.print(f"\n[bold green]Data saved to:[/bold green] {output_csv}")

    # Print summary
    console.print("\n[bold]Summary Statistics[/bold]")
    console.print(f"Total records: {len(df)}")
    console.print(f"Year range: {df['year'].min()} - {df['year'].max()}")
    console.print(f"Periods: {', '.join(sorted(df['period'].unique()))}")
    console.print(f"Regions: {', '.join(sorted(df['region'].unique()))}")
    console.print(f"Unique species: {df['species'].nunique()}")

    # Display sample data
    console.print("\n[bold]Sample Data (first 10 records):[/bold]")
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Year")
    table.add_column("Period")
    table.add_column("Region")
    table.add_column("Species")
    table.add_column("Product")
    table.add_column("Low")
    table.add_column("High")
    table.add_column("Unit")

    for _, row in df.head(10).iterrows():
        table.add_row(
            str(row['year']),
            row['period'],
            row['region'],
            row['species'][:30],  # Truncate long species names
            row['product_type'][:20] if row['product_type'] else '',
            f"${row['price_low']:.2f}" if pd.notna(row['price_low']) else '',
            f"${row['price_high']:.2f}" if pd.notna(row['price_high']) else '',
            row['unit']
        )

    console.print(table)

    # Show records by year and period
    console.print("\n[bold]Records by Year and Period:[/bold]")
    year_period_counts = df.groupby(['year', 'period']).size().sort_index()
    for (year, period), count in year_period_counts.items():
        console.print(f"  {year} {period}: {count} records")


if __name__ == "__main__":
    main()

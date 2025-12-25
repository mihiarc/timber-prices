"""Integrate USFS PNW stumpage data into the unified dataset.

The USFS PNW Research Station publishes historical stumpage prices from
National Forest timber sales. This is ADMINISTERED pricing, not market prices.

Data sources:
- usfs_pnw_stumpage_combined.csv: Regional averages by subregion
- usfs_pnw_species_stumpage.csv: Species-specific prices

Output: Appends to data/processed/stumpage_unified.csv
"""

import pandas as pd
from pathlib import Path
from rich.console import Console
from rich.table import Table

console = Console()

# Paths
RAW_DIR = Path("data/raw/usfs_pnw")
UNIFIED_PATH = Path("data/processed/stumpage_unified.csv")

# Region to state mapping
REGION_TO_STATES = {
    "Montana_Idaho": ["MT", "ID"],
    "Washington_Oregon": ["WA", "OR"],
    "California": ["CA"],
    "Alaska": ["AK"],
    "Northern_Region_MT_ID": ["MT", "ID"],
}

# Subregion to state mapping (more specific)
SUBREGION_TO_STATE = {
    # Individual states
    "Montana": "MT",
    "Idaho": "ID",
    "Washington": "WA",
    "Oregon": "OR",
    "California": "CA",
    "Alaska": "AK",
    # Combined regions from combined file
    "Montana_Idaho": "MT_ID",
    "Washington_Oregon": "WA_OR",
    # USFS Region names from species file
    "Northern_Region_MT_ID": "MT_ID",
    "Intermountain_Region": "ID",  # R4 - primarily Idaho portions
    "Pacific_Northwest_WA_OR": "WA_OR",
    "Pacific_Southwest_CA": "CA",
}

# Species standardization
SPECIES_MAP = {
    "Douglas-fir": "douglas_fir",
    "Ponderosa pine": "ponderosa_pine",
    "Western white pine": "white_pine",
    "Lodgepole pine": "lodgepole_pine",
    "Engelmann spruce": "engelmann_spruce",
    "Western hemlock": "western_hemlock",
    "Cedars": "cedar",
    "Larch": "western_larch",
    "True firs": "true_fir",
    "All species": "all_species",
    "Western redcedar": "western_redcedar",
    "Sitka spruce": "sitka_spruce",
    "Red alder": "red_alder",
    "Other hardwoods": "hardwood_other",
    "Other softwoods": "softwood_other",
}

# MBF to tons conversion (rough average for softwood sawtimber)
# 1 MBF ≈ 3.5-4.5 tons depending on species. Using 4.0 as average.
MBF_TO_TONS = 4.0


def load_combined_data() -> pd.DataFrame:
    """Load the combined regional stumpage data."""
    path = RAW_DIR / "usfs_pnw_stumpage_combined.csv"
    df = pd.read_csv(path)
    console.print(f"[blue]Loaded combined data:[/blue] {len(df)} rows")
    return df


def load_species_data() -> pd.DataFrame:
    """Load the species-specific stumpage data."""
    path = RAW_DIR / "usfs_pnw_species_stumpage.csv"
    df = pd.read_csv(path)
    console.print(f"[blue]Loaded species data:[/blue] {len(df)} rows")
    return df


def transform_combined(df: pd.DataFrame) -> pd.DataFrame:
    """Transform combined data to unified schema."""
    rows = []

    for _, row in df.iterrows():
        year = row["year"]
        region = row["region"]
        subregion = row.get("subregion", region)
        price_mbf = row["price_per_mbf"]
        table = row.get("table", "")

        # Skip if no valid price
        if pd.isna(price_mbf):
            continue

        # Determine state code
        if subregion in SUBREGION_TO_STATE:
            state = SUBREGION_TO_STATE[subregion]
        elif region in SUBREGION_TO_STATE:
            state = SUBREGION_TO_STATE[region]
        else:
            # Default to region name as-is
            state = region.replace("_", "-")

        # Calculate price per ton
        price_per_ton = price_mbf / MBF_TO_TONS

        rows.append({
            "source": state,
            "year": int(year),
            "quarter": None,
            "period_type": "annual",
            "region": subregion if subregion != region else "Statewide",
            "county": None,
            "species": "all_species",
            "product_type": "sawtimber",
            "price_avg": price_mbf,
            "price_low": None,
            "price_high": None,
            "unit": "$/MBF",
            "price_per_ton": round(price_per_ton, 2),
            "conversion_factor": MBF_TO_TONS,
            "sample_size": None,
            "notes": f"USFS PNW National Forest stumpage. {table}. Administered pricing, not market.",
        })

    return pd.DataFrame(rows)


def transform_species(df: pd.DataFrame) -> pd.DataFrame:
    """Transform species-specific data to unified schema."""
    rows = []

    for _, row in df.iterrows():
        year = row["year"]
        region = row["region"]
        species_raw = row["species"]
        price_mbf = row["price_per_mbf"]
        table = row.get("table", "")

        # Skip if no valid price
        if pd.isna(price_mbf):
            continue

        # Standardize species name
        species = SPECIES_MAP.get(species_raw, species_raw.lower().replace(" ", "_"))

        # Determine state code from region
        if region in SUBREGION_TO_STATE:
            state = SUBREGION_TO_STATE[region]
        elif region in REGION_TO_STATES:
            # Use combined code for multi-state regions
            states = REGION_TO_STATES[region]
            state = "_".join(states)
        else:
            state = region.replace("_", "-")

        # Calculate price per ton
        price_per_ton = price_mbf / MBF_TO_TONS

        rows.append({
            "source": state,
            "year": int(year),
            "quarter": None,
            "period_type": "annual",
            "region": region.replace("_", " "),
            "county": None,
            "species": species,
            "product_type": "sawtimber",
            "price_avg": price_mbf,
            "price_low": None,
            "price_high": None,
            "unit": "$/MBF",
            "price_per_ton": round(price_per_ton, 2),
            "conversion_factor": MBF_TO_TONS,
            "sample_size": None,
            "notes": f"USFS PNW National Forest stumpage. {table}. Administered pricing, not market.",
        })

    return pd.DataFrame(rows)


def show_summary(df: pd.DataFrame, title: str):
    """Display summary statistics."""
    table = Table(title=title)
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="green")

    table.add_row("Total rows", str(len(df)))
    table.add_row("Year range", f"{df['year'].min()} - {df['year'].max()}")
    table.add_row("States", ", ".join(sorted(df["source"].unique())))
    table.add_row("Species", str(df["species"].nunique()))

    console.print(table)


def main():
    console.print("[bold]Integrating USFS PNW stumpage data[/bold]\n")

    # Load raw data
    combined_df = load_combined_data()
    species_df = load_species_data()

    # Transform to unified schema
    console.print("\n[yellow]Transforming data...[/yellow]")
    combined_unified = transform_combined(combined_df)
    species_unified = transform_species(species_df)

    # Combine both
    usfs_pnw_unified = pd.concat([combined_unified, species_unified], ignore_index=True)

    # Remove duplicates (prefer species-specific over combined)
    usfs_pnw_unified = usfs_pnw_unified.drop_duplicates(
        subset=["source", "year", "species", "region"],
        keep="last"
    )

    show_summary(usfs_pnw_unified, "USFS PNW Data Transformed")

    # Load existing unified dataset
    console.print("\n[yellow]Loading existing unified dataset...[/yellow]")
    existing_df = pd.read_csv(UNIFIED_PATH)
    console.print(f"[blue]Existing rows:[/blue] {len(existing_df)}")

    # Check for existing USFS PNW data
    existing_usfs = existing_df[existing_df["notes"].str.contains("USFS PNW", na=False)]
    if len(existing_usfs) > 0:
        console.print(f"[yellow]Found {len(existing_usfs)} existing USFS PNW rows - removing to avoid duplicates[/yellow]")
        existing_df = existing_df[~existing_df["notes"].str.contains("USFS PNW", na=False)]

    # Append new data
    unified_df = pd.concat([existing_df, usfs_pnw_unified], ignore_index=True)

    # Sort by source, year
    unified_df = unified_df.sort_values(["source", "year", "quarter"], na_position="last")

    # Save
    unified_df.to_csv(UNIFIED_PATH, index=False)
    console.print(f"\n[green]Saved unified dataset:[/green] {len(unified_df)} total rows")

    # Show final summary
    console.print("\n[bold]Integration complete![/bold]")
    console.print(f"  Added: {len(usfs_pnw_unified)} USFS PNW rows")
    console.print(f"  Total: {len(unified_df)} rows in unified dataset")

    # Show state coverage
    console.print("\n[bold]USFS PNW Coverage by State:[/bold]")
    state_summary = usfs_pnw_unified.groupby("source").agg({
        "year": ["min", "max", "count"],
        "species": "nunique"
    }).round(0)
    state_summary.columns = ["first_year", "last_year", "rows", "species"]
    console.print(state_summary.to_string())


if __name__ == "__main__":
    main()

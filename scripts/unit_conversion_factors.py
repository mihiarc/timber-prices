#!/usr/bin/env python3
"""
Timber Unit Conversion Factors

This module contains conversion factors for standardizing timber stumpage prices
to a common unit ($/ton). All factors are derived from authoritative forestry sources.

Sources:
--------
1. Mississippi State University Extension Service
   - "Pine Timber Volume-to-Weight Conversions" (Publication P2244)
     https://extension.msstate.edu/publications/pine-timber-volume-weight-conversions
   - "Hardwood Timber Volume-to-Weight Conversions" (Publication P3448)
     https://extension.msstate.edu/publications/hardwood-timber-volume-weight-conversions

2. USDA Forest Service
   - "Timber Products Monitoring: Unit of Measure Conversion Factors" (GTR-SRS-251)
     https://www.srs.fs.usda.gov/pubs/gtr/gtr_srs251.pdf

3. Penn State Extension
   - "Conversions Commonly Used When Comparing Timber and Carbon Values"
     https://extension.psu.edu/conversions-commonly-used-when-comparing-timber-and-carbon-values

Definitions:
-----------
- 1 ton = 2,000 pounds (short ton)
- 1 cord = 128 cubic feet of stacked roundwood (4' x 4' x 8')
- 1 MBF = 1,000 board feet (Doyle, Scribner, or International 1/4" log rule)

Notes:
------
- Conversion factors vary by species, tree diameter, moisture content, and season
- Values below represent typical/average factors used in commercial transactions
- MBF conversions assume average diameter timber (16-20" DBH)
- Cord conversions assume standard pulpwood specifications
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class ConversionFactor:
    """Represents a unit conversion factor with metadata."""
    factor: float           # Conversion factor (tons per unit)
    unit_from: str         # Original unit
    unit_to: str           # Target unit (always 'ton')
    species_group: str     # Pine, Hardwood, Mixed
    product_type: str      # Sawtimber, Pulpwood, etc.
    source: str            # Citation
    notes: Optional[str] = None


# =============================================================================
# CORD TO TON CONVERSION FACTORS
# =============================================================================
# These factors convert $/cord to $/ton
# Formula: price_per_ton = price_per_cord / tons_per_cord

CORD_TO_TON = {
    # Pine species
    'pine_pulpwood': ConversionFactor(
        factor=2.67,
        unit_from='cord',
        unit_to='ton',
        species_group='Pine',
        product_type='Pulpwood',
        source='MSU Extension P2244',
        notes='Average of loblolly/shortleaf (2.6) and longleaf/slash (2.78)'
    ),
    'pine_loblolly_shortleaf': ConversionFactor(
        factor=2.60,
        unit_from='cord',
        unit_to='ton',
        species_group='Pine',
        product_type='Pulpwood',
        source='MSU Extension P2244',
        notes='Loblolly and shortleaf pine pulpwood'
    ),
    'pine_longleaf_slash': ConversionFactor(
        factor=2.78,
        unit_from='cord',
        unit_to='ton',
        species_group='Pine',
        product_type='Pulpwood',
        source='MSU Extension P2244',
        notes='Longleaf and slash pine (higher specific gravity)'
    ),

    # Hardwood species
    'hardwood_soft': ConversionFactor(
        factor=2.70,
        unit_from='cord',
        unit_to='ton',
        species_group='Hardwood',
        product_type='Pulpwood',
        source='MSU Extension P3448; MS Code § 75-27-39',
        notes='Soft hardwoods: sweetgum, yellow poplar'
    ),
    'hardwood_mixed': ConversionFactor(
        factor=2.80,
        unit_from='cord',
        unit_to='ton',
        species_group='Hardwood',
        product_type='Pulpwood',
        source='MSU Extension P3448; MS Code § 75-27-39',
        notes='Mixed hardwood species'
    ),
    'hardwood_hard': ConversionFactor(
        factor=2.90,
        unit_from='cord',
        unit_to='ton',
        species_group='Hardwood',
        product_type='Pulpwood',
        source='MSU Extension P3448; MS Code § 75-27-39',
        notes='Hard hardwoods: oak, hickory'
    ),

    # Default/average values
    'softwood_avg': ConversionFactor(
        factor=2.67,
        unit_from='cord',
        unit_to='ton',
        species_group='Softwood',
        product_type='Pulpwood',
        source='MSU Extension P2244',
        notes='Average for southern pine species'
    ),
    'hardwood_avg': ConversionFactor(
        factor=2.80,
        unit_from='cord',
        unit_to='ton',
        species_group='Hardwood',
        product_type='Pulpwood',
        source='MSU Extension P3448',
        notes='Average for mixed hardwood'
    ),
}


# =============================================================================
# MBF TO TON CONVERSION FACTORS
# =============================================================================
# These factors convert $/MBF to $/ton
# Formula: price_per_ton = price_per_mbf / tons_per_mbf

MBF_TO_TON = {
    # Pine sawtimber by DBH class (tons per MBF)
    'pine_sawtimber_10in': ConversionFactor(
        factor=14.0,
        unit_from='mbf',
        unit_to='ton',
        species_group='Pine',
        product_type='Sawtimber',
        source='MSU Extension P2244',
        notes='10-inch DBH timber'
    ),
    'pine_sawtimber_14in': ConversionFactor(
        factor=8.5,
        unit_from='mbf',
        unit_to='ton',
        species_group='Pine',
        product_type='Sawtimber',
        source='MSU Extension P2244',
        notes='14-inch DBH timber'
    ),
    'pine_sawtimber_18in': ConversionFactor(
        factor=7.2,
        unit_from='mbf',
        unit_to='ton',
        species_group='Pine',
        product_type='Sawtimber',
        source='MSU Extension P2244',
        notes='18-inch DBH timber (typical average)'
    ),
    'pine_sawtimber_24in': ConversionFactor(
        factor=5.9,
        unit_from='mbf',
        unit_to='ton',
        species_group='Pine',
        product_type='Sawtimber',
        source='MSU Extension P2244',
        notes='24-inch DBH timber'
    ),
    'pine_sawtimber_avg': ConversionFactor(
        factor=7.0,
        unit_from='mbf',
        unit_to='ton',
        species_group='Pine',
        product_type='Sawtimber',
        source='MSU Extension P2244',
        notes='Average for typical pine sawtimber (16-20" DBH)'
    ),

    # Hardwood sawtimber by DBH class (tons per MBF)
    'hardwood_sawtimber_14in': ConversionFactor(
        factor=12.1,
        unit_from='mbf',
        unit_to='ton',
        species_group='Hardwood',
        product_type='Sawtimber',
        source='MSU Extension P3448',
        notes='14-inch DBH timber'
    ),
    'hardwood_sawtimber_18in': ConversionFactor(
        factor=9.8,
        unit_from='mbf',
        unit_to='ton',
        species_group='Hardwood',
        product_type='Sawtimber',
        source='MSU Extension P3448',
        notes='18-inch DBH timber'
    ),
    'hardwood_sawtimber_24in': ConversionFactor(
        factor=8.1,
        unit_from='mbf',
        unit_to='ton',
        species_group='Hardwood',
        product_type='Sawtimber',
        source='MSU Extension P3448',
        notes='24-inch DBH timber'
    ),
    'hardwood_sawtimber_avg': ConversionFactor(
        factor=8.5,
        unit_from='mbf',
        unit_to='ton',
        species_group='Hardwood',
        product_type='Sawtimber',
        source='MSU Extension P3448',
        notes='Mills typically use 8-9 tons/MBF for hardwood sawlogs'
    ),
}


# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def get_cord_to_ton_factor(species: str, product_type: str = 'pulpwood') -> float:
    """
    Get the appropriate cord-to-ton conversion factor.

    Args:
        species: Species or species group (pine, oak, maple, mixed, etc.)
        product_type: Product type (pulpwood, cordwood, etc.)

    Returns:
        Conversion factor (tons per cord)
    """
    species_lower = str(species).lower() if species else ''

    # Pine/softwood species
    if any(x in species_lower for x in ['pine', 'spruce', 'fir', 'hemlock', 'cedar', 'softwood']):
        return CORD_TO_TON['pine_pulpwood'].factor

    # Hard hardwoods
    if any(x in species_lower for x in ['oak', 'hickory', 'beech', 'hard maple', 'sugar maple', 'walnut', 'cherry']):
        return CORD_TO_TON['hardwood_hard'].factor

    # Soft hardwoods
    if any(x in species_lower for x in ['poplar', 'tulip', 'sweetgum', 'basswood', 'soft maple', 'aspen', 'cottonwood']):
        return CORD_TO_TON['hardwood_soft'].factor

    # Mixed/default hardwood
    if any(x in species_lower for x in ['hardwood', 'mixed', 'ash', 'birch', 'elm']):
        return CORD_TO_TON['hardwood_mixed'].factor

    # Default to mixed hardwood (middle value)
    return CORD_TO_TON['hardwood_mixed'].factor


def get_mbf_to_ton_factor(species: str, product_type: str = 'sawtimber') -> float:
    """
    Get the appropriate MBF-to-ton conversion factor.

    Args:
        species: Species or species group (pine, oak, maple, mixed, etc.)
        product_type: Product type (sawtimber, veneer, etc.)

    Returns:
        Conversion factor (tons per MBF)
    """
    species_lower = str(species).lower() if species else ''

    # Pine/softwood species
    if any(x in species_lower for x in ['pine', 'spruce', 'fir', 'hemlock', 'cedar', 'softwood']):
        return MBF_TO_TON['pine_sawtimber_avg'].factor

    # Hardwood species (use average)
    return MBF_TO_TON['hardwood_sawtimber_avg'].factor


def convert_to_per_ton(price: float, unit: str, species: str, product_type: str) -> float:
    """
    Convert a price to $/ton.

    Args:
        price: Original price value
        unit: Original unit ($/ton, $/cord, $/mbf, index)
        species: Species or species group
        product_type: Product type

    Returns:
        Price in $/ton (or None if conversion not possible)
    """
    if price is None:
        return None

    unit_lower = str(unit).lower() if unit else ''

    # Already in $/ton
    if 'ton' in unit_lower:
        return price

    # Convert from $/cord
    if 'cord' in unit_lower:
        factor = get_cord_to_ton_factor(species, product_type)
        return price / factor

    # Convert from $/mbf
    if 'mbf' in unit_lower:
        factor = get_mbf_to_ton_factor(species, product_type)
        return price / factor

    # Index values cannot be converted to actual prices
    if 'index' in unit_lower:
        return None

    return None


def print_conversion_table():
    """Print a formatted table of all conversion factors."""
    from rich.console import Console
    from rich.table import Table

    console = Console()

    # Cord to Ton table
    table1 = Table(title="Cord to Ton Conversion Factors")
    table1.add_column("Key", style="cyan")
    table1.add_column("Tons/Cord", justify="right")
    table1.add_column("Species Group")
    table1.add_column("Notes")

    for key, cf in CORD_TO_TON.items():
        table1.add_row(key, f"{cf.factor:.2f}", cf.species_group, cf.notes or "")

    console.print(table1)

    # MBF to Ton table
    table2 = Table(title="\nMBF to Ton Conversion Factors")
    table2.add_column("Key", style="cyan")
    table2.add_column("Tons/MBF", justify="right")
    table2.add_column("Species Group")
    table2.add_column("Notes")

    for key, cf in MBF_TO_TON.items():
        table2.add_row(key, f"{cf.factor:.1f}", cf.species_group, cf.notes or "")

    console.print(table2)


if __name__ == "__main__":
    print_conversion_table()

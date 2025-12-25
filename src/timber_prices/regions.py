"""Timber market region definitions for the United States.

Markets are organized by FOREST TYPE, not just geography. The same state
may participate in multiple distinct markets based on species and products.

For example:
- Maine: Spruce-fir pulpwood market (distinct from Lake States hardwood)
- Michigan UP: Both northern hardwood sawtimber AND aspen pulpwood markets
- North Carolina: Coastal pine AND mountain hardwood markets

Additionally, we track NATIONAL FOREST SYSTEM timber separately. This is not
a true "market" but an administered pricing system with appraised values,
policy constraints, and different data sources. It's significant in the West
where 60%+ of timberland is publicly owned.

Regional Hierarchy:
- Level 1: Major forest type markets (8 private markets + 1 public system)
- Level 2: Geographic sub-markets within forest types
- State participation: States mapped to the markets they participate in

References:
- USFS FIA Forest Type Groups
- TimberMart-South product categories
- Forisk wood basket analysis
- Academic market integration research
- USFS Timber Sale Program (Cut & Sold reports)
"""

from enum import Enum
from typing import NamedTuple


class TimberMarket(str, Enum):
    """Major timber markets defined by forest type and primary products."""

    # Softwood Markets
    SOUTHERN_PINE = "southern_pine"
    """Loblolly, slash, longleaf pine. SE US. Sawtimber, pulp, chip-n-saw.
    Short rotation (25-35 yr). World's most productive planted forests."""

    DOUGLAS_FIR = "douglas_fir"
    """Douglas-fir, western hemlock, western red cedar. PNW west of Cascades.
    Premium sawtimber, veneer. Highest volume/acre in North America."""

    WESTERN_PINE = "western_pine"
    """Ponderosa, lodgepole pine. PNW east side, Northern Rockies.
    Sawtimber focus. Fire-adapted, longer rotations."""

    SPRUCE_FIR = "spruce_fir"
    """Spruce, balsam fir. Maine, northern NH/VT, Upper Great Lakes.
    Pulpwood dominant. Distinct from hardwood markets in same geography."""

    # Hardwood Markets
    APPALACHIAN_HARDWOOD = "appalachian_hardwood"
    """White oak, red oak, cherry, walnut, yellow poplar. Central Appalachians.
    Premium sawtimber, veneer, export. Highest value hardwoods."""

    NORTHERN_HARDWOOD = "northern_hardwood"
    """Sugar maple, red maple, beech, birch. Lake States, Northeast uplands.
    Sawtimber, veneer. Distinct from pulpwood markets in same region."""

    OAK_HICKORY = "oak_hickory"
    """White oak, red oak, hickory. Central hardwoods - MO, IN, southern IL/OH.
    Sawtimber focus. Bourbon barrel staves, flooring."""

    # Pulpwood-Specific Markets
    ASPEN_PULP = "aspen_pulp"
    """Aspen, paper birch. Lake States. Pulpwood for OSB, paper.
    Short rotation. Distinct market from northern hardwood sawtimber."""

    # Administered Public Timber (not a true market)
    NATIONAL_FOREST = "national_forest"
    """US National Forest System timber sales. NOT a true market - administered
    pricing based on appraisal, policy constraints, and public objectives.
    Significant in West (60%+ public ownership). Includes USFS Regions 1-6.
    Data: Cut & Sold reports, timber sale records. Prices reflect appraised
    value, road credits, stewardship contracts - not pure stumpage."""


class MarketProduct(str, Enum):
    """Primary product types in timber markets."""

    SAWTIMBER = "sawtimber"
    PULPWOOD = "pulpwood"
    CHIP_N_SAW = "chip_n_saw"
    VENEER = "veneer"
    POLES = "poles"


class GeographicZone(str, Enum):
    """Geographic zones for sub-market delineation."""

    # Southern Pine zones
    SOUTH_ATLANTIC_COASTAL = "south_atlantic_coastal"  # GA, SC, NC coastal, FL
    SOUTH_ATLANTIC_PIEDMONT = "south_atlantic_piedmont"  # GA, SC, NC piedmont
    GULF_COASTAL = "gulf_coastal"  # AL, MS, LA, TX east
    GULF_INTERIOR = "gulf_interior"  # AR south, LA north

    # Douglas-fir zones
    PACIFIC_NORTHWEST_COAST = "pnw_coast"  # OR, WA coast and west Cascades
    PACIFIC_SOUTHWEST_COAST = "pac_sw_coast"  # CA redwood belt

    # Western pine zones
    INLAND_NORTHWEST = "inland_northwest"  # OR, WA east, ID north, MT west
    NORTHERN_ROCKIES = "northern_rockies"  # MT, ID central

    # Spruce-fir zones
    NORTHERN_NEW_ENGLAND = "northern_new_england"  # ME, NH, VT
    UPPER_GREAT_LAKES = "upper_great_lakes"  # MI UP, northern WI, northern MN

    # Appalachian hardwood zones
    CENTRAL_APPALACHIAN = "central_appalachian"  # WV, VA mountains, eastern KY
    NORTHERN_APPALACHIAN = "northern_appalachian"  # PA, NY southern tier

    # Northern hardwood zones
    LAKE_STATES_HARDWOOD = "lake_states_hardwood"  # MI, WI, MN (hardwood component)
    NORTHEAST_HARDWOOD = "northeast_hardwood"  # NY, VT, NH, ME (hardwood component)

    # Oak-hickory zones
    OZARK_OUACHITA = "ozark_ouachita"  # MO, AR north, OK east
    CENTRAL_HARDWOOD = "central_hardwood"  # IN, OH, IL south

    # Aspen-pulp zones
    LAKE_STATES_ASPEN = "lake_states_aspen"  # MN, WI, MI aspen resource

    # National Forest System - USFS Administrative Regions
    USFS_R1_NORTHERN = "usfs_r1_northern"  # MT, ID (north), ND, SD (partial)
    USFS_R2_ROCKY_MOUNTAIN = "usfs_r2_rocky_mtn"  # CO, WY, SD, NE, KS
    USFS_R3_SOUTHWESTERN = "usfs_r3_southwestern"  # AZ, NM
    USFS_R4_INTERMOUNTAIN = "usfs_r4_intermountain"  # UT, NV, ID (south), WY (west)
    USFS_R5_PACIFIC_SOUTHWEST = "usfs_r5_pacific_sw"  # CA, HI, Pacific Islands
    USFS_R6_PACIFIC_NORTHWEST = "usfs_r6_pacific_nw"  # OR, WA
    USFS_R8_SOUTHERN = "usfs_r8_southern"  # 13 Southern states, PR, USVI
    USFS_R9_EASTERN = "usfs_r9_eastern"  # 20 Northeastern/Midwestern states
    USFS_R10_ALASKA = "usfs_r10_alaska"  # AK (Tongass, Chugach)


class MarketDefinition(NamedTuple):
    """Defines a timber market's characteristics."""

    market: TimberMarket
    primary_species: list[str]
    primary_products: list[MarketProduct]
    typical_rotation_years: int
    geographic_zones: list[GeographicZone]
    states: list[str]
    private_ownership_pct: int
    notes: str


# Complete market definitions
MARKET_DEFINITIONS: dict[TimberMarket, MarketDefinition] = {
    TimberMarket.SOUTHERN_PINE: MarketDefinition(
        market=TimberMarket.SOUTHERN_PINE,
        primary_species=["loblolly_pine", "slash_pine", "longleaf_pine", "shortleaf_pine"],
        primary_products=[MarketProduct.SAWTIMBER, MarketProduct.PULPWOOD, MarketProduct.CHIP_N_SAW],
        typical_rotation_years=28,
        geographic_zones=[
            GeographicZone.SOUTH_ATLANTIC_COASTAL,
            GeographicZone.SOUTH_ATLANTIC_PIEDMONT,
            GeographicZone.GULF_COASTAL,
            GeographicZone.GULF_INTERIOR,
        ],
        states=["AL", "AR", "FL", "GA", "LA", "MS", "NC", "SC", "TX", "VA"],
        private_ownership_pct=90,
        notes="61% of US timber removals. TimberMart-South coverage. World's wood basket.",
    ),
    TimberMarket.DOUGLAS_FIR: MarketDefinition(
        market=TimberMarket.DOUGLAS_FIR,
        primary_species=["douglas_fir", "western_hemlock", "western_red_cedar", "sitka_spruce"],
        primary_products=[MarketProduct.SAWTIMBER, MarketProduct.VENEER, MarketProduct.PULPWOOD],
        typical_rotation_years=45,
        geographic_zones=[
            GeographicZone.PACIFIC_NORTHWEST_COAST,
            GeographicZone.PACIFIC_SOUTHWEST_COAST,
        ],
        states=["OR", "WA", "CA"],
        private_ownership_pct=40,
        notes="Highest productivity in North America. Strong export to Asia. Delivered log prices common.",
    ),
    TimberMarket.WESTERN_PINE: MarketDefinition(
        market=TimberMarket.WESTERN_PINE,
        primary_species=["ponderosa_pine", "lodgepole_pine", "western_larch"],
        primary_products=[MarketProduct.SAWTIMBER],
        typical_rotation_years=80,
        geographic_zones=[
            GeographicZone.INLAND_NORTHWEST,
            GeographicZone.NORTHERN_ROCKIES,
        ],
        states=["OR", "WA", "ID", "MT"],
        private_ownership_pct=30,
        notes="East of Cascades. National Forest dominant. Fire-adapted management.",
    ),
    TimberMarket.SPRUCE_FIR: MarketDefinition(
        market=TimberMarket.SPRUCE_FIR,
        primary_species=["red_spruce", "white_spruce", "balsam_fir", "black_spruce"],
        primary_products=[MarketProduct.PULPWOOD, MarketProduct.SAWTIMBER],
        typical_rotation_years=60,
        geographic_zones=[
            GeographicZone.NORTHERN_NEW_ENGLAND,
            GeographicZone.UPPER_GREAT_LAKES,
        ],
        states=["ME", "NH", "VT", "MI", "MN", "WI"],
        private_ownership_pct=75,
        notes="Pulpwood focus. Distinct from hardwood markets in same geography. Paper/packaging.",
    ),
    TimberMarket.APPALACHIAN_HARDWOOD: MarketDefinition(
        market=TimberMarket.APPALACHIAN_HARDWOOD,
        primary_species=["white_oak", "red_oak", "black_cherry", "black_walnut", "yellow_poplar", "sugar_maple"],
        primary_products=[MarketProduct.SAWTIMBER, MarketProduct.VENEER],
        typical_rotation_years=80,
        geographic_zones=[
            GeographicZone.CENTRAL_APPALACHIAN,
            GeographicZone.NORTHERN_APPALACHIAN,
        ],
        states=["WV", "VA", "KY", "TN", "PA", "NY", "OH", "MD"],
        private_ownership_pct=85,
        notes="Premium hardwoods. Export market. Veneer, furniture, flooring. Highest $/MBF.",
    ),
    TimberMarket.NORTHERN_HARDWOOD: MarketDefinition(
        market=TimberMarket.NORTHERN_HARDWOOD,
        primary_species=["sugar_maple", "red_maple", "american_beech", "yellow_birch", "white_ash"],
        primary_products=[MarketProduct.SAWTIMBER, MarketProduct.VENEER, MarketProduct.PULPWOOD],
        typical_rotation_years=70,
        geographic_zones=[
            GeographicZone.LAKE_STATES_HARDWOOD,
            GeographicZone.NORTHEAST_HARDWOOD,
        ],
        states=["MI", "MN", "WI", "NY", "VT", "NH", "ME", "PA"],
        private_ownership_pct=80,
        notes="Maple syrup integration. Furniture, flooring. Distinct from spruce-fir pulp.",
    ),
    TimberMarket.OAK_HICKORY: MarketDefinition(
        market=TimberMarket.OAK_HICKORY,
        primary_species=["white_oak", "red_oak", "shagbark_hickory", "black_walnut"],
        primary_products=[MarketProduct.SAWTIMBER, MarketProduct.VENEER],
        typical_rotation_years=75,
        geographic_zones=[
            GeographicZone.OZARK_OUACHITA,
            GeographicZone.CENTRAL_HARDWOOD,
        ],
        states=["MO", "AR", "IN", "OH", "IL", "OK", "KS"],
        private_ownership_pct=85,
        notes="Bourbon barrel staves (white oak). Flooring. Distinct from Appalachian premium.",
    ),
    TimberMarket.ASPEN_PULP: MarketDefinition(
        market=TimberMarket.ASPEN_PULP,
        primary_species=["quaking_aspen", "bigtooth_aspen", "paper_birch"],
        primary_products=[MarketProduct.PULPWOOD],
        typical_rotation_years=40,
        geographic_zones=[
            GeographicZone.LAKE_STATES_ASPEN,
        ],
        states=["MN", "WI", "MI"],
        private_ownership_pct=65,
        notes="OSB, paper, packaging. Short rotation. Distinct from hardwood sawtimber market.",
    ),
    # =========================================================================
    # ADMINISTERED PUBLIC TIMBER (not a true market)
    # =========================================================================
    TimberMarket.NATIONAL_FOREST: MarketDefinition(
        market=TimberMarket.NATIONAL_FOREST,
        primary_species=["all_species"],  # Varies by region
        primary_products=[MarketProduct.SAWTIMBER, MarketProduct.PULPWOOD],
        typical_rotation_years=0,  # Policy-driven, not rotation-based
        geographic_zones=[
            GeographicZone.USFS_R1_NORTHERN,
            GeographicZone.USFS_R2_ROCKY_MOUNTAIN,
            GeographicZone.USFS_R3_SOUTHWESTERN,
            GeographicZone.USFS_R4_INTERMOUNTAIN,
            GeographicZone.USFS_R5_PACIFIC_SOUTHWEST,
            GeographicZone.USFS_R6_PACIFIC_NORTHWEST,
            GeographicZone.USFS_R8_SOUTHERN,
            GeographicZone.USFS_R9_EASTERN,
            GeographicZone.USFS_R10_ALASKA,
        ],
        states=[
            # R1 Northern
            "MT", "ID",
            # R2 Rocky Mountain
            "CO", "WY", "SD", "NE",
            # R3 Southwestern
            "AZ", "NM",
            # R4 Intermountain
            "UT", "NV",
            # R5 Pacific Southwest
            "CA",
            # R6 Pacific Northwest
            "OR", "WA",
            # R8 Southern (all have some NF land)
            "AL", "AR", "FL", "GA", "KY", "LA", "MS", "NC", "OK", "SC", "TN", "TX", "VA",
            # R9 Eastern
            "IL", "IN", "ME", "MI", "MN", "MO", "NH", "NY", "OH", "PA", "VT", "WI", "WV",
            # R10 Alaska
            "AK",
        ],
        private_ownership_pct=0,  # 100% public by definition
        notes="""NOT a true market. Administered pricing via timber sale appraisal.
        Prices reflect appraised stumpage, purchaser road credits, stewardship
        contracts, and salvage sales. Supply is policy-constrained (NFMA, ESA,
        roadless rules), not market-responsive. Data: USFS Cut & Sold reports,
        timber sale contract records. Most significant in R1, R4, R5, R6 (West)
        where National Forests dominate timberland ownership.""",
    ),
}


class StateMarketParticipation(NamedTuple):
    """Maps a state to the timber markets it participates in."""

    state: str
    primary_market: TimberMarket
    secondary_markets: list[TimberMarket]
    tms_regions: list[str] | None  # TimberMart-South codes (South only)
    intrastate_zones: list[str]  # State-specific market subdivisions
    notes: str


# State-to-market participation mapping
# Key insight: States participate in MULTIPLE markets based on forest types present
STATE_MARKET_PARTICIPATION: dict[str, StateMarketParticipation] = {
    # ==========================================================================
    # SOUTHERN PINE STATES (may also have hardwood markets)
    # ==========================================================================
    "GA": StateMarketParticipation(
        state="GA",
        primary_market=TimberMarket.SOUTHERN_PINE,
        secondary_markets=[TimberMarket.APPALACHIAN_HARDWOOD],  # North GA mountains
        tms_regions=["GA1", "GA2"],
        intrastate_zones=["Coastal Plain", "Piedmont", "Mountains"],
        notes="GA1=South pine, GA2=North (more hardwood). County-level data available.",
    ),
    "AL": StateMarketParticipation(
        state="AL",
        primary_market=TimberMarket.SOUTHERN_PINE,
        secondary_markets=[TimberMarket.APPALACHIAN_HARDWOOD],  # NE Alabama
        tms_regions=["AL1", "AL2"],
        intrastate_zones=["North", "South"],
        notes="AL1=North (hardwood mix), AL2=South (pine dominant)",
    ),
    "MS": StateMarketParticipation(
        state="MS",
        primary_market=TimberMarket.SOUTHERN_PINE,
        secondary_markets=[TimberMarket.OAK_HICKORY],  # Delta bottomlands
        tms_regions=["MS1", "MS2"],
        intrastate_zones=["Delta/North", "Piney Woods/South"],
        notes="MS2 Piney Woods is core pine market",
    ),
    "LA": StateMarketParticipation(
        state="LA",
        primary_market=TimberMarket.SOUTHERN_PINE,
        secondary_markets=[],  # Cypress is minor
        tms_regions=["LA1", "LA2"],
        intrastate_zones=["North", "South"],
        notes="LA1=North pine core, LA2=South coastal/cypress",
    ),
    "TX": StateMarketParticipation(
        state="TX",
        primary_market=TimberMarket.SOUTHERN_PINE,
        secondary_markets=[TimberMarket.OAK_HICKORY],  # East TX hardwood
        tms_regions=["TX1", "TX2"],
        intrastate_zones=["Northeast TX", "Southeast TX"],
        notes="East Texas only. TX2 Southeast is pine core.",
    ),
    "AR": StateMarketParticipation(
        state="AR",
        primary_market=TimberMarket.SOUTHERN_PINE,  # South AR
        secondary_markets=[TimberMarket.OAK_HICKORY],  # Ozarks
        tms_regions=["AR1", "AR2"],
        intrastate_zones=["Ozarks/North", "Gulf Coastal Plain/South"],
        notes="AR1=Ozark hardwood, AR2=Gulf Coastal pine",
    ),
    "NC": StateMarketParticipation(
        state="NC",
        primary_market=TimberMarket.SOUTHERN_PINE,  # Coastal Plain
        secondary_markets=[TimberMarket.APPALACHIAN_HARDWOOD],  # Mountains
        tms_regions=["NC1", "NC2"],
        intrastate_zones=["Mountains", "Piedmont", "Coastal Plain"],
        notes="NC1=Mountains (hardwood), NC2=Coastal Plain (pine). Excellent data.",
    ),
    "SC": StateMarketParticipation(
        state="SC",
        primary_market=TimberMarket.SOUTHERN_PINE,
        secondary_markets=[TimberMarket.APPALACHIAN_HARDWOOD],  # Upstate
        tms_regions=["SC1", "SC2"],
        intrastate_zones=["Lowcountry", "Upstate"],
        notes="SC2=Lowcountry pine core",
    ),
    "FL": StateMarketParticipation(
        state="FL",
        primary_market=TimberMarket.SOUTHERN_PINE,
        secondary_markets=[],
        tms_regions=["FL1", "FL2"],
        intrastate_zones=["Panhandle", "Peninsula"],
        notes="FL1=Panhandle (more productive), FL2=Peninsula",
    ),
    "VA": StateMarketParticipation(
        state="VA",
        primary_market=TimberMarket.SOUTHERN_PINE,  # Coastal/Piedmont
        secondary_markets=[TimberMarket.APPALACHIAN_HARDWOOD],  # Mountains
        tms_regions=["VA1", "VA2"],
        intrastate_zones=["Mountains", "Piedmont", "Coastal"],
        notes="VA1=Mountains (Appalachian market), VA2=Piedmont/Coastal (pine)",
    ),

    # ==========================================================================
    # APPALACHIAN / OAK-HICKORY HARDWOOD STATES
    # ==========================================================================
    "WV": StateMarketParticipation(
        state="WV",
        primary_market=TimberMarket.APPALACHIAN_HARDWOOD,
        secondary_markets=[],
        tms_regions=None,
        intrastate_zones=["Region 1", "Region 2", "Region 3", "Region 4", "Region 5"],
        notes="Premium Appalachian hardwoods. 5 forestry regions. High-value export.",
    ),
    "KY": StateMarketParticipation(
        state="KY",
        primary_market=TimberMarket.APPALACHIAN_HARDWOOD,  # Eastern KY
        secondary_markets=[TimberMarket.OAK_HICKORY],  # Western KY
        tms_regions=None,
        intrastate_zones=["Eastern", "Western"],
        notes="Split between Appalachian (east) and Central Hardwood (west)",
    ),
    "TN": StateMarketParticipation(
        state="TN",
        primary_market=TimberMarket.APPALACHIAN_HARDWOOD,  # East TN
        secondary_markets=[TimberMarket.OAK_HICKORY, TimberMarket.SOUTHERN_PINE],
        tms_regions=["TN1", "TN2"],
        intrastate_zones=["East", "Middle", "West"],
        notes="TN1=East (Appalachian), TN2=West (bottomland hardwood, some pine)",
    ),
    "OH": StateMarketParticipation(
        state="OH",
        primary_market=TimberMarket.APPALACHIAN_HARDWOOD,  # SE Ohio
        secondary_markets=[TimberMarket.OAK_HICKORY, TimberMarket.NORTHERN_HARDWOOD],
        tms_regions=None,
        intrastate_zones=["Northeast", "Northwest", "South"],
        notes="SE=Appalachian hardwood, NW=oak-hickory transition, NE=northern hardwood edge",
    ),
    "MO": StateMarketParticipation(
        state="MO",
        primary_market=TimberMarket.OAK_HICKORY,
        secondary_markets=[],
        tms_regions=None,
        intrastate_zones=["North", "South (Ozarks)"],
        notes="Ozark hardwoods. White oak for bourbon barrels.",
    ),
    "IN": StateMarketParticipation(
        state="IN",
        primary_market=TimberMarket.OAK_HICKORY,
        secondary_markets=[TimberMarket.NORTHERN_HARDWOOD],  # North
        tms_regions=None,
        intrastate_zones=["North", "South"],
        notes="Central hardwoods. Walnut, oak focus.",
    ),
    "PA": StateMarketParticipation(
        state="PA",
        primary_market=TimberMarket.NORTHERN_HARDWOOD,
        secondary_markets=[TimberMarket.APPALACHIAN_HARDWOOD],  # SW PA
        tms_regions=None,
        intrastate_zones=["Northwest", "Northeast", "Southwest", "Southeast"],
        notes="Major hardwood producer. Penn State quarterly reports. Cherry, maple.",
    ),

    # ==========================================================================
    # LAKE STATES (Multiple distinct markets!)
    # ==========================================================================
    "MI": StateMarketParticipation(
        state="MI",
        primary_market=TimberMarket.NORTHERN_HARDWOOD,  # Hardwood sawtimber
        secondary_markets=[TimberMarket.ASPEN_PULP, TimberMarket.SPRUCE_FIR],
        tms_regions=None,
        intrastate_zones=["Upper Peninsula", "Northern Lower Peninsula", "Southern LP"],
        notes="UP=spruce-fir + hardwood, NLP=aspen + hardwood. Three distinct markets.",
    ),
    "WI": StateMarketParticipation(
        state="WI",
        primary_market=TimberMarket.ASPEN_PULP,  # Major OSB/pulp
        secondary_markets=[TimberMarket.NORTHERN_HARDWOOD, TimberMarket.SPRUCE_FIR],
        tms_regions=None,
        intrastate_zones=["North", "Central", "South"],
        notes="Strong aspen pulp industry. Northern hardwood sawtimber secondary.",
    ),
    "MN": StateMarketParticipation(
        state="MN",
        primary_market=TimberMarket.ASPEN_PULP,
        secondary_markets=[TimberMarket.SPRUCE_FIR, TimberMarket.NORTHERN_HARDWOOD],
        tms_regions=None,
        intrastate_zones=["Northeast", "North Central", "Northwest"],
        notes="Aspen dominant. Some spruce-fir in arrowhead. Limited hardwood sawtimber.",
    ),

    # ==========================================================================
    # NORTHEAST (Spruce-fir pulp vs. Northern hardwood)
    # ==========================================================================
    "ME": StateMarketParticipation(
        state="ME",
        primary_market=TimberMarket.SPRUCE_FIR,  # Pulpwood focus
        secondary_markets=[TimberMarket.NORTHERN_HARDWOOD],  # Some maple/birch
        tms_regions=None,
        intrastate_zones=["North Woods", "Central", "Southern"],
        notes="Spruce-fir pulpwood dominant. Paper industry. Distinct from Lake States hardwood.",
    ),
    "NH": StateMarketParticipation(
        state="NH",
        primary_market=TimberMarket.NORTHERN_HARDWOOD,
        secondary_markets=[TimberMarket.SPRUCE_FIR],  # White Mountains
        tms_regions=None,
        intrastate_zones=["North Country", "Lakes Region", "South"],
        notes="White pine also significant. DRA reports.",
    ),
    "VT": StateMarketParticipation(
        state="VT",
        primary_market=TimberMarket.NORTHERN_HARDWOOD,
        secondary_markets=[TimberMarket.SPRUCE_FIR],
        tms_regions=None,
        intrastate_zones=["Northeast Kingdom", "Central", "Southern"],
        notes="Sugar maple focus. Integrated with syrup industry. Quarterly FPR data.",
    ),
    "NY": StateMarketParticipation(
        state="NY",
        primary_market=TimberMarket.NORTHERN_HARDWOOD,
        secondary_markets=[TimberMarket.APPALACHIAN_HARDWOOD, TimberMarket.SPRUCE_FIR],
        tms_regions=None,
        intrastate_zones=["Adirondack", "Catskills", "Hudson-Mohawk", "Western-Central"],
        notes="4 distinct market regions. Adirondacks=spruce-fir + hardwood.",
    ),

    # ==========================================================================
    # PACIFIC NORTHWEST
    # ==========================================================================
    "OR": StateMarketParticipation(
        state="OR",
        primary_market=TimberMarket.DOUGLAS_FIR,  # West side
        secondary_markets=[TimberMarket.WESTERN_PINE],  # East side
        tms_regions=None,
        intrastate_zones=["Coast", "Willamette Valley", "Cascades West", "East Oregon"],
        notes="Cascade divide. West=Douglas-fir, East=ponderosa. USFS PNW data.",
    ),
    "WA": StateMarketParticipation(
        state="WA",
        primary_market=TimberMarket.DOUGLAS_FIR,
        secondary_markets=[TimberMarket.WESTERN_PINE],
        tms_regions=None,
        intrastate_zones=["Coast", "Puget Sound", "Cascades West", "East Washington"],
        notes="Similar east-west divide as Oregon.",
    ),
    "CA": StateMarketParticipation(
        state="CA",
        primary_market=TimberMarket.DOUGLAS_FIR,  # North coast
        secondary_markets=[TimberMarket.WESTERN_PINE],  # Sierra
        tms_regions=None,
        intrastate_zones=["Redwood Coast", "Klamath", "Sierra Nevada"],
        notes="Redwood is unique species. Limited public stumpage data.",
    ),
    "ID": StateMarketParticipation(
        state="ID",
        primary_market=TimberMarket.WESTERN_PINE,
        secondary_markets=[TimberMarket.DOUGLAS_FIR],  # North ID
        tms_regions=None,
        intrastate_zones=["North", "Central", "South"],
        notes="North ID more productive. South ID limited timber.",
    ),
    "MT": StateMarketParticipation(
        state="MT",
        primary_market=TimberMarket.WESTERN_PINE,
        secondary_markets=[],
        tms_regions=None,
        intrastate_zones=["Western", "Central"],
        notes="Ponderosa, lodgepole, Douglas-fir. National Forest dominant.",
    ),
}


# TimberMart-South coverage
TMS_STATES = ["AL", "AR", "FL", "GA", "LA", "MS", "NC", "SC", "TN", "TX", "VA"]

# Core TMS regions (90% of pine removals)
TMS_CORE_REGIONS = [
    "AL1", "AL2", "AR2", "FL2", "GA1", "GA2",
    "LA1", "MS1", "MS2", "NC2", "SC2", "TX2"
]


def get_market_states(market: TimberMarket) -> list[str]:
    """Get all states participating in a market (primary or secondary)."""
    states = []
    for state, participation in STATE_MARKET_PARTICIPATION.items():
        if participation.primary_market == market or market in participation.secondary_markets:
            states.append(state)
    return sorted(states)


def get_primary_market_states(market: TimberMarket) -> list[str]:
    """Get states where this is the PRIMARY market."""
    return sorted([
        state for state, p in STATE_MARKET_PARTICIPATION.items()
        if p.primary_market == market
    ])


def get_state_markets(state: str) -> list[TimberMarket]:
    """Get all markets a state participates in."""
    if state not in STATE_MARKET_PARTICIPATION:
        return []
    p = STATE_MARKET_PARTICIPATION[state]
    return [p.primary_market] + p.secondary_markets


# Market characteristics for analysis
MARKET_CHARACTERISTICS = {
    market: {
        "primary_species": defn.primary_species,
        "primary_products": [p.value for p in defn.primary_products],
        "rotation_years": defn.typical_rotation_years,
        "ownership_private_pct": defn.private_ownership_pct,
        "geographic_zones": [z.value for z in defn.geographic_zones],
        "states": defn.states,
    }
    for market, defn in MARKET_DEFINITIONS.items()
}


# =============================================================================
# USFS NATIONAL FOREST SYSTEM - Administrative Regions
# =============================================================================

class USFSRegion(NamedTuple):
    """USFS Administrative Region for National Forest timber."""

    region_number: int
    name: str
    states: list[str]
    headquarters: str
    major_forests: list[str]
    timber_significance: str  # "high", "moderate", "low"
    notes: str


USFS_REGIONS: dict[int, USFSRegion] = {
    1: USFSRegion(
        region_number=1,
        name="Northern Region",
        states=["MT", "ID", "ND", "SD"],  # ND/SD partial
        headquarters="Missoula, MT",
        major_forests=["Flathead", "Lolo", "Nez Perce-Clearwater", "Idaho Panhandle"],
        timber_significance="high",
        notes="Significant timber program. Lodgepole, ponderosa, Douglas-fir.",
    ),
    2: USFSRegion(
        region_number=2,
        name="Rocky Mountain Region",
        states=["CO", "WY", "SD", "NE", "KS"],
        headquarters="Lakewood, CO",
        major_forests=["White River", "Arapaho-Roosevelt", "Medicine Bow-Routt"],
        timber_significance="moderate",
        notes="Mixed use. Beetle salvage significant. Lodgepole, spruce-fir.",
    ),
    3: USFSRegion(
        region_number=3,
        name="Southwestern Region",
        states=["AZ", "NM"],
        headquarters="Albuquerque, NM",
        major_forests=["Apache-Sitgreaves", "Gila", "Lincoln", "Coconino"],
        timber_significance="low",
        notes="Limited commercial timber. Ponderosa pine. Fire/restoration focus.",
    ),
    4: USFSRegion(
        region_number=4,
        name="Intermountain Region",
        states=["UT", "NV", "ID", "WY"],  # Southern ID, western WY
        headquarters="Ogden, UT",
        major_forests=["Boise", "Sawtooth", "Salmon-Challis", "Bridger-Teton"],
        timber_significance="moderate",
        notes="Mixed conifer. Some significant timber in ID portions.",
    ),
    5: USFSRegion(
        region_number=5,
        name="Pacific Southwest Region",
        states=["CA", "HI"],
        headquarters="Vallejo, CA",
        major_forests=["Six Rivers", "Shasta-Trinity", "Sierra", "Sequoia"],
        timber_significance="high",
        notes="Significant historical timber. Reduced by spotted owl, fires. Mixed conifer.",
    ),
    6: USFSRegion(
        region_number=6,
        name="Pacific Northwest Region",
        states=["OR", "WA"],
        headquarters="Portland, OR",
        major_forests=["Mt. Hood", "Willamette", "Deschutes", "Olympic", "Gifford Pinchot"],
        timber_significance="high",
        notes="Historically largest timber region. Douglas-fir. Reduced by NW Forest Plan.",
    ),
    8: USFSRegion(
        region_number=8,
        name="Southern Region",
        states=["AL", "AR", "FL", "GA", "KY", "LA", "MS", "NC", "OK", "SC", "TN", "TX", "VA", "PR", "VI"],
        headquarters="Atlanta, GA",
        major_forests=["Ouachita", "Ozark", "Francis Marion", "Nantahala", "Cherokee"],
        timber_significance="moderate",
        notes="Smaller NF footprint in private-dominated region. Pine, hardwood mix.",
    ),
    9: USFSRegion(
        region_number=9,
        name="Eastern Region",
        states=["IL", "IN", "IA", "ME", "MI", "MN", "MO", "NH", "NY", "OH", "PA", "VT", "WI", "WV"],
        headquarters="Milwaukee, WI",
        major_forests=["Allegheny", "Green Mountain", "White Mountain", "Chequamegon-Nicolet", "Chippewa"],
        timber_significance="moderate",
        notes="Fragmented NF lands. Northern hardwood, spruce-fir. Hiawatha significant in MI.",
    ),
    10: USFSRegion(
        region_number=10,
        name="Alaska Region",
        states=["AK"],
        headquarters="Juneau, AK",
        major_forests=["Tongass", "Chugach"],
        timber_significance="moderate",
        notes="Tongass historically significant. Sitka spruce, hemlock. Reduced by Roadless Rule.",
    ),
}


def get_usfs_region(state: str) -> list[int]:
    """Get USFS Region number(s) for a state.

    Some states span multiple regions (e.g., ID spans R1 and R4).
    """
    regions = []
    for region_num, region in USFS_REGIONS.items():
        if state in region.states:
            regions.append(region_num)
    return sorted(regions)


def get_usfs_region_states(region_number: int) -> list[str]:
    """Get states in a USFS Region."""
    if region_number not in USFS_REGIONS:
        return []
    return USFS_REGIONS[region_number].states


# States where National Forest timber is a SIGNIFICANT source
# (>20% of total timber harvest from NF lands)
NF_SIGNIFICANT_STATES = [
    "MT", "ID", "OR", "WA", "CA",  # Western states with high NF %
    "AK",  # Tongass/Chugach
    "CO", "AZ", "NM",  # Rocky Mountain/Southwest (smaller volume but high % public)
]

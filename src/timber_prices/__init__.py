"""Timber prices data collection package."""

__version__ = "0.1.0"

from timber_prices.config import get_settings, Settings, STUMPAGE_SOURCES
from timber_prices.regions import (
    # Market enums and types
    TimberMarket,
    MarketProduct,
    GeographicZone,
    # Market definitions
    MARKET_DEFINITIONS,
    STATE_MARKET_PARTICIPATION,
    MARKET_CHARACTERISTICS,
    # Market lookup functions
    get_market_states,
    get_primary_market_states,
    get_state_markets,
    # TimberMart-South
    TMS_STATES,
    TMS_CORE_REGIONS,
    # National Forest System
    USFSRegion,
    USFS_REGIONS,
    get_usfs_region,
    get_usfs_region_states,
    NF_SIGNIFICANT_STATES,
)

__all__ = [
    # Config
    "get_settings",
    "Settings",
    "STUMPAGE_SOURCES",
    # Markets (forest-type driven)
    "TimberMarket",
    "MarketProduct",
    "GeographicZone",
    "MARKET_DEFINITIONS",
    "STATE_MARKET_PARTICIPATION",
    "get_market_states",
    "get_primary_market_states",
    "get_state_markets",
    "MARKET_CHARACTERISTICS",
    # TimberMart-South
    "TMS_STATES",
    "TMS_CORE_REGIONS",
    # National Forest System (administered pricing, not true market)
    "USFSRegion",
    "USFS_REGIONS",
    "get_usfs_region",
    "get_usfs_region_states",
    "NF_SIGNIFICANT_STATES",
]

"""
Application Configuration
Central configuration for validation rules and constants
"""

# ============================================================================
# VALIDATION CONSTRAINTS (Backend Safety Limits)
# ============================================================================

# Rainfall delta constraints (%)
# Conservative limits based on climate research
RAIN_DELTA_MIN = -50.0  # Max 50% decrease (severe drought)
RAIN_DELTA_MAX = 30.0   # Max 30% increase (extreme flooding)

# Temperature delta constraints (°C)
# Based on IPCC projections for 2100
TEMP_DELTA_MIN = -2.0   # Cooling scenario
TEMP_DELTA_MAX = 5.0    # Extreme warming (RCP8.5+)

# Urban growth constraints (%)
# Based on historical urbanization rates
URBAN_GROWTH_MIN = 0.0    # No growth
URBAN_GROWTH_MAX = 100.0  # 100% expansion (doubling)

# Year constraints
TARGET_YEAR_MIN = 2025
TARGET_YEAR_MAX = 2100

# Region constraints
MAX_REGION_AREA_KM2 = 500000  # 500,000 km² max (prevents quota exhaustion)

# ============================================================================
# APPLICATION SETTINGS
# ============================================================================

# Cache settings
CACHE_MAX_SIZE = 100        # Maximum cached scenarios
CACHE_TTL_HOURS = 24        # Cache time-to-live

# Earth Engine settings
GEE_SCALE_METERS = 1000     # Resolution for GEE queries
GEE_MAX_PIXELS = 1e9        # Max pixels per query

# Simulation settings
BASELINE_YEAR = 2020        # Fixed baseline year for consistency

# ============================================================================
# ERROR MESSAGES
# ============================================================================

ERROR_MESSAGES = {
    'rain_delta_range': f"Rainfall delta must be between {RAIN_DELTA_MIN}% and {RAIN_DELTA_MAX}%",
    'temp_delta_range': f"Temperature delta must be between {TEMP_DELTA_MIN}°C and {TEMP_DELTA_MAX}°C",
    'urban_growth_range': f"Urban growth must be between {URBAN_GROWTH_MIN}% and {URBAN_GROWTH_MAX}%",
    'year_range': f"Target year must be between {TARGET_YEAR_MIN} and {TARGET_YEAR_MAX}",
    'invalid_region': "Invalid region specified",
}

# ============================================================================
# ACADEMIC DISCLAIMER
# ============================================================================

SIMULATION_DISCLAIMER = """
This system generates SIMULATIONS, not predictions.

Results represent one possible future under specified conditions,
not a forecast of actual outcomes.

For academic and research purposes only.
"""

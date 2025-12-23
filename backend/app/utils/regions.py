"""
Region definitions and utilities
"""
import ee
from typing import Dict, List


# Predefined regions with their bounding boxes
REGIONS = {
    'Tamil Nadu': {
        'bbox': [77.0, 8.0, 80.5, 13.5],
        'center': [78.75, 10.75],
        'description': 'Tamil Nadu state, India'
    },
    'Karnataka': {
        'bbox': [74.0, 11.5, 78.5, 18.5],
        'center': [76.25, 15.0],
        'description': 'Karnataka state, India'
    },
    'Kerala': {
        'bbox': [74.8, 8.2, 77.4, 12.8],
        'center': [76.1, 10.5],
        'description': 'Kerala state, India'
    },
    'India': {
        'bbox': [68.0, 6.0, 97.0, 36.0],
        'center': [82.5, 21.0],
        'description': 'India (full country)'
    },
    'test': {
        'bbox': [78.46, 20.09, 79.46, 21.09],
        'center': [78.96, 20.59],
        'description': 'Test region (central India, ~100km x 100km)'
    }
}


def _normalize_region_name(region_id: str) -> str:
    """Convert region ID to display name"""
    # Build mapping of id -> display name
    id_to_name = {key.lower().replace(' ', ''): key for key in REGIONS.keys()}
    return id_to_name.get(region_id, region_id)


def get_region_geometry(region_name: str) -> ee.Geometry:
    """
    Get Earth Engine geometry for a named region
    
    Args:
        region_name: Name or ID of the region (e.g., 'test' or 'Tamil Nadu')
        
    Returns:
        ee.Geometry object
        
    Raises:
        ValueError: If region not found
    """
    # Try to normalize the name first
    display_name = _normalize_region_name(region_name)
    
    if display_name not in REGIONS:
        available = ', '.join(REGIONS.keys())
        raise ValueError(f"Region '{region_name}' not found. Available: {available}")
    
    bbox = REGIONS[display_name]['bbox']
    return ee.Geometry.Rectangle(bbox)


def get_available_regions() -> List[Dict]:
    """Get list of available regions with metadata"""
    result = []
    for key, value in REGIONS.items():
        result.append({
            "id": key.lower().replace(' ', ''),
            "name": key,
            "bbox": value['bbox'],
            "description": value.get('description', '')
        })
    return result

def get_available_region_names() -> List[str]:
    """Get list of available region names only"""
    return [key.lower().replace(' ', '') for key in REGIONS.keys()]


def get_region_info(region_name: str) -> Dict:
    """
    Get information about a region
    
    Args:
        region_name: Name or ID of the region
        
    Returns:
        Dictionary with region metadata
    """
    # Normalize the name
    display_name = _normalize_region_name(region_name)
    
    if display_name not in REGIONS:
        raise ValueError(f"Region '{region_name}' not found")
    
    return REGIONS[display_name]


def validate_year(year: int) -> bool:
    """
    Validate if year is within acceptable range for data
    
    Args:
        year: Year to validate
        
    Returns:
        True if valid, False otherwise
    """
    return 2010 <= year <= 2024


def calculate_region_area(region: ee.Geometry) -> float:
    """
    Calculate area of a region in square kilometers
    
    Args:
        region: Earth Engine geometry
        
    Returns:
        Area in km²
    """
    area_m2 = region.area().getInfo()
    area_km2 = area_m2 / 1_000_000
    return area_km2

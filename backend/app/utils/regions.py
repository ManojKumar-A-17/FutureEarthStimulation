"""
Region definitions and utilities
"""
import ee
from typing import Dict, List


# Predefined regions with their bounding boxes
REGIONS = {
    # INDIA - States
    'Andhra Pradesh': {
        'bbox': [76.8, 12.6, 84.8, 19.9],
        'center': [80.8, 16.25],
        'description': 'Andhra Pradesh state, India'
    },
    'Arunachal Pradesh': {
        'bbox': [91.6, 26.6, 97.4, 29.5],
        'center': [94.5, 28.05],
        'description': 'Arunachal Pradesh state, India'
    },
    'Assam': {
        'bbox': [89.7, 24.1, 96.0, 28.0],
        'center': [92.85, 26.05],
        'description': 'Assam state, India'
    },
    'Bihar': {
        'bbox': [83.3, 24.3, 88.3, 27.5],
        'center': [85.8, 25.9],
        'description': 'Bihar state, India'
    },
    'Chhattisgarh': {
        'bbox': [80.3, 17.8, 84.4, 24.1],
        'center': [82.35, 20.95],
        'description': 'Chhattisgarh state, India'
    },
    'Goa': {
        'bbox': [73.7, 14.9, 74.4, 15.8],
        'center': [74.05, 15.35],
        'description': 'Goa state, India'
    },
    'Gujarat': {
        'bbox': [68.2, 20.1, 74.5, 24.7],
        'center': [71.35, 22.4],
        'description': 'Gujarat state, India'
    },
    'Haryana': {
        'bbox': [74.5, 27.7, 77.6, 30.9],
        'center': [76.05, 29.3],
        'description': 'Haryana state, India'
    },
    'Himachal Pradesh': {
        'bbox': [75.6, 30.4, 79.0, 33.2],
        'center': [77.3, 31.8],
        'description': 'Himachal Pradesh state, India'
    },
    'Jharkhand': {
        'bbox': [83.3, 21.9, 87.6, 25.3],
        'center': [85.45, 23.6],
        'description': 'Jharkhand state, India'
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
    'Madhya Pradesh': {
        'bbox': [74.0, 21.1, 82.8, 26.9],
        'center': [78.4, 24.0],
        'description': 'Madhya Pradesh state, India'
    },
    'Maharashtra': {
        'bbox': [72.6, 15.6, 80.9, 22.0],
        'center': [76.75, 18.8],
        'description': 'Maharashtra state, India'
    },
    'Manipur': {
        'bbox': [93.0, 23.8, 94.8, 25.7],
        'center': [93.9, 24.75],
        'description': 'Manipur state, India'
    },
    'Meghalaya': {
        'bbox': [89.8, 25.0, 92.8, 26.1],
        'center': [91.3, 25.55],
        'description': 'Meghalaya state, India'
    },
    'Mizoram': {
        'bbox': [92.2, 21.9, 93.5, 24.5],
        'center': [92.85, 23.2],
        'description': 'Mizoram state, India'
    },
    'Nagaland': {
        'bbox': [93.3, 25.2, 95.2, 27.0],
        'center': [94.25, 26.1],
        'description': 'Nagaland state, India'
    },
    'Odisha': {
        'bbox': [81.4, 17.8, 87.5, 22.6],
        'center': [84.45, 20.2],
        'description': 'Odisha state, India'
    },
    'Punjab': {
        'bbox': [73.9, 29.5, 76.9, 32.6],
        'center': [75.4, 31.05],
        'description': 'Punjab state, India'
    },
    'Rajasthan': {
        'bbox': [69.5, 23.0, 78.3, 30.2],
        'center': [73.9, 26.6],
        'description': 'Rajasthan state, India'
    },
    'Sikkim': {
        'bbox': [87.9, 27.1, 88.9, 28.1],
        'center': [88.4, 27.6],
        'description': 'Sikkim state, India'
    },
    'Tamil Nadu': {
        'bbox': [77.0, 8.0, 80.5, 13.5],
        'center': [78.75, 10.75],
        'description': 'Tamil Nadu state, India'
    },
    'Telangana': {
        'bbox': [77.2, 15.8, 81.3, 19.9],
        'center': [79.25, 17.85],
        'description': 'Telangana state, India'
    },
    'Tripura': {
        'bbox': [91.0, 22.9, 92.5, 24.5],
        'center': [91.75, 23.7],
        'description': 'Tripura state, India'
    },
    'Uttar Pradesh': {
        'bbox': [77.1, 23.9, 84.6, 30.4],
        'center': [80.85, 27.15],
        'description': 'Uttar Pradesh state, India'
    },
    'Uttarakhand': {
        'bbox': [77.6, 28.7, 81.0, 31.5],
        'center': [79.3, 30.1],
        'description': 'Uttarakhand state, India'
    },
    'West Bengal': {
        'bbox': [85.8, 21.5, 89.9, 27.2],
        'center': [87.85, 24.35],
        'description': 'West Bengal state, India'
    },
    'India': {
        'bbox': [68.0, 6.0, 97.0, 36.0],
        'center': [82.5, 21.0],
        'description': 'India (full country)'
    },
    
    # UNITED STATES - States
    'California': {
        'bbox': [-124.4, 32.5, -114.1, 42.0],
        'center': [-119.25, 37.25],
        'description': 'California state, USA'
    },
    'Texas': {
        'bbox': [-106.6, 25.8, -93.5, 36.5],
        'center': [-100.05, 31.15],
        'description': 'Texas state, USA'
    },
    'Florida': {
        'bbox': [-87.6, 24.5, -80.0, 31.0],
        'center': [-83.8, 27.75],
        'description': 'Florida state, USA'
    },
    'New York': {
        'bbox': [-79.8, 40.5, -71.9, 45.0],
        'center': [-75.85, 42.75],
        'description': 'New York state, USA'
    },
    'Pennsylvania': {
        'bbox': [-80.5, 39.7, -74.7, 42.3],
        'center': [-77.6, 41.0],
        'description': 'Pennsylvania state, USA'
    },
    'Illinois': {
        'bbox': [-91.5, 36.9, -87.5, 42.5],
        'center': [-89.5, 39.7],
        'description': 'Illinois state, USA'
    },
    'Ohio': {
        'bbox': [-84.8, 38.4, -80.5, 42.3],
        'center': [-82.65, 40.35],
        'description': 'Ohio state, USA'
    },
    'Georgia': {
        'bbox': [-85.6, 30.4, -80.8, 35.0],
        'center': [-83.2, 32.7],
        'description': 'Georgia state, USA'
    },
    'North Carolina': {
        'bbox': [-84.3, 33.8, -75.5, 36.6],
        'center': [-79.9, 35.2],
        'description': 'North Carolina state, USA'
    },
    'Michigan': {
        'bbox': [-90.4, 41.7, -82.4, 48.2],
        'center': [-86.4, 44.95],
        'description': 'Michigan state, USA'
    },
    'United States': {
        'bbox': [-125.0, 24.5, -66.9, 49.4],
        'center': [-95.95, 36.95],
        'description': 'United States (contiguous)'
    },
    
    # CHINA - Provinces
    'Guangdong': {
        'bbox': [109.7, 20.2, 117.2, 25.5],
        'center': [113.45, 22.85],
        'description': 'Guangdong province, China'
    },
    'Shandong': {
        'bbox': [114.8, 34.4, 122.7, 38.4],
        'center': [118.75, 36.4],
        'description': 'Shandong province, China'
    },
    'Henan': {
        'bbox': [110.4, 31.4, 116.6, 36.4],
        'center': [113.5, 33.9],
        'description': 'Henan province, China'
    },
    'Sichuan': {
        'bbox': [97.3, 26.0, 108.5, 34.3],
        'center': [102.9, 30.15],
        'description': 'Sichuan province, China'
    },
    'Jiangsu': {
        'bbox': [116.4, 30.7, 121.9, 35.1],
        'center': [119.15, 32.9],
        'description': 'Jiangsu province, China'
    },
    'Hebei': {
        'bbox': [113.5, 36.0, 119.8, 42.6],
        'center': [116.65, 39.3],
        'description': 'Hebei province, China'
    },
    'Hunan': {
        'bbox': [108.8, 24.6, 114.3, 30.1],
        'center': [111.55, 27.35],
        'description': 'Hunan province, China'
    },
    'Anhui': {
        'bbox': [114.9, 29.4, 119.7, 34.7],
        'center': [117.3, 32.05],
        'description': 'Anhui province, China'
    },
    'Hubei': {
        'bbox': [108.4, 29.0, 116.1, 33.3],
        'center': [112.25, 31.15],
        'description': 'Hubei province, China'
    },
    'Zhejiang': {
        'bbox': [118.0, 27.0, 123.0, 31.2],
        'center': [120.5, 29.1],
        'description': 'Zhejiang province, China'
    },
    'China': {
        'bbox': [73.5, 18.2, 135.0, 53.6],
        'center': [104.25, 35.9],
        'description': 'China (full country)'
    },
    
    # BRAZIL - States
    'São Paulo': {
        'bbox': [-53.1, -25.3, -44.2, -19.8],
        'center': [-48.65, -22.55],
        'description': 'São Paulo state, Brazil'
    },
    'Minas Gerais': {
        'bbox': [-51.0, -22.9, -39.9, -14.2],
        'center': [-45.45, -18.55],
        'description': 'Minas Gerais state, Brazil'
    },
    'Bahia': {
        'bbox': [-46.6, -18.3, -37.3, -8.5],
        'center': [-41.95, -13.4],
        'description': 'Bahia state, Brazil'
    },
    'Rio de Janeiro': {
        'bbox': [-44.9, -23.4, -40.9, -20.8],
        'center': [-42.9, -22.1],
        'description': 'Rio de Janeiro state, Brazil'
    },
    'Paraná': {
        'bbox': [-54.6, -26.7, -48.0, -22.5],
        'center': [-51.3, -24.6],
        'description': 'Paraná state, Brazil'
    },
    'Rio Grande do Sul': {
        'bbox': [-57.6, -33.8, -49.7, -27.1],
        'center': [-53.65, -30.45],
        'description': 'Rio Grande do Sul state, Brazil'
    },
    'Pará': {
        'bbox': [-58.9, -9.8, -46.0, -2.5],
        'center': [-52.45, -6.15],
        'description': 'Pará state, Brazil'
    },
    'Amazonas': {
        'bbox': [-73.8, -9.8, -56.1, -2.1],
        'center': [-64.95, -5.95],
        'description': 'Amazonas state, Brazil'
    },
    'Brazil': {
        'bbox': [-73.9, -33.8, -34.8, 5.3],
        'center': [-54.35, -14.25],
        'description': 'Brazil (full country)'
    },
    
    # AUSTRALIA - States
    'New South Wales': {
        'bbox': [141.0, -37.5, 153.6, -28.2],
        'center': [147.3, -32.85],
        'description': 'New South Wales state, Australia'
    },
    'Queensland': {
        'bbox': [138.0, -29.2, 153.6, -10.7],
        'center': [145.8, -19.95],
        'description': 'Queensland state, Australia'
    },
    'Victoria': {
        'bbox': [141.0, -39.2, 149.9, -34.0],
        'center': [145.45, -36.6],
        'description': 'Victoria state, Australia'
    },
    'Western Australia': {
        'bbox': [113.0, -35.1, 129.0, -13.7],
        'center': [121.0, -24.4],
        'description': 'Western Australia state, Australia'
    },
    'South Australia': {
        'bbox': [129.0, -38.1, 141.0, -26.0],
        'center': [135.0, -32.05],
        'description': 'South Australia state, Australia'
    },
    'Australia': {
        'bbox': [113.0, -43.6, 153.6, -10.7],
        'center': [133.3, -27.15],
        'description': 'Australia (full country)'
    },
    
    # EUROPE - Select Countries
    'United Kingdom': {
        'bbox': [-8.6, 49.9, 1.8, 60.8],
        'center': [-3.4, 55.35],
        'description': 'United Kingdom (full country)'
    },
    'France': {
        'bbox': [-5.1, 41.3, 9.6, 51.1],
        'center': [2.25, 46.2],
        'description': 'France (full country)'
    },
    'Germany': {
        'bbox': [5.9, 47.3, 15.0, 55.1],
        'center': [10.45, 51.2],
        'description': 'Germany (full country)'
    },
    'Italy': {
        'bbox': [6.6, 36.6, 18.5, 47.1],
        'center': [12.55, 41.85],
        'description': 'Italy (full country)'
    },
    'Spain': {
        'bbox': [-9.3, 35.9, 4.3, 43.8],
        'center': [-2.5, 39.85],
        'description': 'Spain (full country)'
    },
    
    # AFRICA - Select Countries
    'Nigeria': {
        'bbox': [2.7, 4.3, 14.7, 13.9],
        'center': [8.7, 9.1],
        'description': 'Nigeria (full country)'
    },
    'South Africa': {
        'bbox': [16.5, -34.8, 32.9, -22.1],
        'center': [24.7, -28.45],
        'description': 'South Africa (full country)'
    },
    'Kenya': {
        'bbox': [33.9, -4.7, 41.9, 5.5],
        'center': [37.9, 0.4],
        'description': 'Kenya (full country)'
    },
    'Egypt': {
        'bbox': [24.7, 22.0, 36.9, 31.7],
        'center': [30.8, 26.85],
        'description': 'Egypt (full country)'
    },
    
    # SOUTH AMERICA - Additional Countries
    'Argentina': {
        'bbox': [-73.6, -55.1, -53.6, -21.8],
        'center': [-63.6, -38.45],
        'description': 'Argentina (full country)'
    },
    'Colombia': {
        'bbox': [-79.0, -4.2, -66.9, 12.5],
        'center': [-72.95, 4.15],
        'description': 'Colombia (full country)'
    },
    
    # SOUTHEAST ASIA
    'Indonesia': {
        'bbox': [95.0, -11.0, 141.0, 6.0],
        'center': [118.0, -2.5],
        'description': 'Indonesia (full country)'
    },
    'Thailand': {
        'bbox': [97.3, 5.6, 105.6, 20.5],
        'center': [101.45, 13.05],
        'description': 'Thailand (full country)'
    },
    'Vietnam': {
        'bbox': [102.1, 8.6, 109.5, 23.4],
        'center': [105.8, 16.0],
        'description': 'Vietnam (full country)'
    },
    'Philippines': {
        'bbox': [116.9, 4.6, 126.6, 21.1],
        'center': [121.75, 12.85],
        'description': 'Philippines (full country)'
    },
    
    # JAPAN
    'Japan': {
        'bbox': [129.4, 30.9, 145.8, 45.5],
        'center': [137.6, 38.2],
        'description': 'Japan (full country)'
    },
    
    # CANADA - Provinces
    'Ontario': {
        'bbox': [-95.2, 41.7, -74.3, 56.9],
        'center': [-84.75, 49.3],
        'description': 'Ontario province, Canada'
    },
    'Quebec': {
        'bbox': [-79.8, 45.0, -57.1, 62.6],
        'center': [-68.45, 53.8],
        'description': 'Quebec province, Canada'
    },
    'British Columbia': {
        'bbox': [-139.1, 48.3, -114.0, 60.0],
        'center': [-126.55, 54.15],
        'description': 'British Columbia province, Canada'
    },
    'Canada': {
        'bbox': [-141.0, 41.7, -52.6, 83.1],
        'center': [-96.8, 62.4],
        'description': 'Canada (full country)'
    },
    
    # MEXICO
    'Mexico': {
        'bbox': [-118.4, 14.5, -86.7, 32.7],
        'center': [-102.55, 23.6],
        'description': 'Mexico (full country)'
    },
    
    # TEST REGION
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

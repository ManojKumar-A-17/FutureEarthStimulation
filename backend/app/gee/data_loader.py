"""
Google Earth Engine Data Loader
Fetches real satellite and climate data for simulation
"""
import ee
import numpy as np
from typing import Dict, Tuple, Optional


class GEEDataLoader:
    """Loads and processes Earth observation data from Google Earth Engine"""
    
    def __init__(self):
        """Initialize data loader with dataset configurations"""
        self.datasets = {
            'land_cover': 'GOOGLE/DYNAMICWORLD/V1',
            'rainfall': 'UCSB-CHG/CHIRPS/DAILY',
            'temperature': 'MODIS/006/MOD11A1',
            'ndvi': 'MODIS/006/MOD13A2',
            'nightlights': 'NOAA/VIIRS/DNB/MONTHLY_V1/VCMSLCFG',
            'population': 'WorldPop/GP/100m/pop'
        }
    
    def get_region_geometry(self, region_name: str) -> ee.Geometry:
        """
        Get geometry for named region
        
        Args:
            region_name: Name of region (e.g., 'Tamil Nadu', 'India')
            
        Returns:
            Earth Engine Geometry object
        """
        # Import regions from utils
        from app.utils.regions import REGIONS
        
        if region_name not in REGIONS:
            raise ValueError(f"Region '{region_name}' not found. Available: {list(REGIONS.keys())}")
        
        bbox = REGIONS[region_name]['bbox']
        return ee.Geometry.Rectangle(bbox)
    
    def fetch_land_cover(
        self, 
        region: ee.Geometry, 
        year: int = 2020,
        scale: int = 1000
    ) -> Dict:
        """
        Fetch land cover classification from Dynamic World
        
        Args:
            region: Earth Engine geometry for the area
            year: Year of data (2020-2024)
            scale: Resolution in meters
            
        Returns:
            Dictionary with land cover statistics
        """
        start_date = f'{year}-01-01'
        end_date = f'{year}-12-31'
        
        # Load Dynamic World dataset
        dw = ee.ImageCollection(self.datasets['land_cover']) \
            .filterDate(start_date, end_date) \
            .filterBounds(region) \
            .select('label') \
            .mode()  # Most common class per pixel
        
        # Calculate class areas
        class_areas = dw.reduceRegion(
            reducer=ee.Reducer.frequencyHistogram(),
            geometry=region,
            scale=scale,
            maxPixels=1e9
        ).getInfo()
        
        return {
            'year': year,
            'classes': class_areas.get('label', {}),
            'metadata': {
                'scale': scale,
                'dataset': 'Dynamic World'
            }
        }
    
    def fetch_rainfall(
        self, 
        region: ee.Geometry, 
        year: int = 2020,
        scale: int = 5000
    ) -> Dict:
        """
        Fetch rainfall data from CHIRPS
        
        Args:
            region: Earth Engine geometry
            year: Year of data
            scale: Resolution in meters
            
        Returns:
            Annual rainfall statistics
        """
        start_date = f'{year}-01-01'
        end_date = f'{year}-12-31'
        
        # Load CHIRPS precipitation
        rainfall = ee.ImageCollection(self.datasets['rainfall']) \
            .filterDate(start_date, end_date) \
            .filterBounds(region) \
            .select('precipitation') \
            .sum()  # Total annual rainfall
        
        stats = rainfall.reduceRegion(
            reducer=ee.Reducer.mean().combine(
                reducer2=ee.Reducer.stdDev(),
                sharedInputs=True
            ),
            geometry=region,
            scale=scale,
            maxPixels=1e9
        ).getInfo()
        
        return {
            'year': year,
            'annual_mean_mm': stats.get('precipitation_mean', 0),
            'std_dev_mm': stats.get('precipitation_stdDev', 0),
            'metadata': {
                'scale': scale,
                'dataset': 'CHIRPS'
            }
        }
    
    def fetch_temperature(
        self, 
        region: ee.Geometry, 
        year: int = 2020,
        scale: int = 1000
    ) -> Dict:
        """
        Fetch land surface temperature from MODIS
        
        Args:
            region: Earth Engine geometry
            year: Year of data
            scale: Resolution in meters
            
        Returns:
            Temperature statistics in Celsius
        """
        start_date = f'{year}-01-01'
        end_date = f'{year}-12-31'
        
        # Load MODIS LST
        lst = ee.ImageCollection(self.datasets['temperature']) \
            .filterDate(start_date, end_date) \
            .filterBounds(region) \
            .select('LST_Day_1km') \
            .mean()
        
        # Convert from Kelvin to Celsius (MODIS LST is in Kelvin * 0.02)
        lst_celsius = lst.multiply(0.02).subtract(273.15)
        
        stats = lst_celsius.reduceRegion(
            reducer=ee.Reducer.mean().combine(
                reducer2=ee.Reducer.stdDev(),
                sharedInputs=True
            ),
            geometry=region,
            scale=scale,
            maxPixels=1e9
        ).getInfo()
        
        return {
            'year': year,
            'mean_celsius': stats.get('LST_Day_1km_mean', 0),
            'std_dev_celsius': stats.get('LST_Day_1km_stdDev', 0),
            'metadata': {
                'scale': scale,
                'dataset': 'MODIS LST'
            }
        }
    
    def fetch_ndvi(
        self, 
        region: ee.Geometry, 
        year: int = 2020,
        scale: int = 1000
    ) -> Dict:
        """
        Fetch vegetation health (NDVI) from MODIS
        
        Args:
            region: Earth Engine geometry
            year: Year of data
            scale: Resolution in meters
            
        Returns:
            NDVI statistics (-1 to 1, higher = healthier vegetation)
        """
        start_date = f'{year}-01-01'
        end_date = f'{year}-12-31'
        
        # Load MODIS NDVI
        ndvi = ee.ImageCollection(self.datasets['ndvi']) \
            .filterDate(start_date, end_date) \
            .filterBounds(region) \
            .select('NDVI') \
            .mean()
        
        # Scale NDVI (MODIS NDVI has scale factor 0.0001)
        ndvi_scaled = ndvi.multiply(0.0001)
        
        stats = ndvi_scaled.reduceRegion(
            reducer=ee.Reducer.mean().combine(
                reducer2=ee.Reducer.stdDev(),
                sharedInputs=True
            ),
            geometry=region,
            scale=scale,
            maxPixels=1e9
        ).getInfo()
        
        return {
            'year': year,
            'mean_ndvi': stats.get('NDVI_mean', 0),
            'std_dev_ndvi': stats.get('NDVI_stdDev', 0),
            'metadata': {
                'scale': scale,
                'dataset': 'MODIS NDVI'
            }
        }
    
    def fetch_baseline_state(
        self,
        region_name: str,
        year: int = 2020
    ) -> Dict:
        """
        Fetch complete baseline Earth state for a region
        
        Args:
            region_name: Name of region
            year: Base year for data
            
        Returns:
            Complete dataset with all layers
        """
        region = self.get_region_geometry(region_name)
        
        return {
            'region': region_name,
            'year': year,
            'land_cover': self.fetch_land_cover(region, year),
            'rainfall': self.fetch_rainfall(region, year),
            'temperature': self.fetch_temperature(region, year),
            'ndvi': self.fetch_ndvi(region, year)
        }

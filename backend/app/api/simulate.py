"""
Production /simulate endpoint
Handles scenario simulation requests from frontend
"""
from fastapi import HTTPException
from typing import Dict, Any

from app.api.models import SimulationRequest, SimulationResponse, SimulationStats, SimulationResults
from app.gee.data_loader import GEEDataLoader
from app.ml.simulation_engine import SimulationEngine
from app.utils.cache import get_cache
from app.utils.regions import get_available_region_names


class SimulateAPI:
    """Handles /simulate endpoint logic"""
    
    def __init__(self):
        """Initialize components"""
        self.data_loader = GEEDataLoader()
        self.simulation_engine = SimulationEngine()
        self.cache = get_cache()
    
    async def run_simulation(self, request: SimulationRequest) -> SimulationResponse:
        """
        Execute simulation for given scenario
        
        Args:
            request: Validated simulation request
            
        Returns:
            Simulation response with results
            
        Raises:
            HTTPException: On validation or execution errors
        """
        # 1. Validate region
        available_regions = get_available_region_names()
        if request.region not in available_regions:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid region. Available: {', '.join(available_regions)}"
            )
        
        # 2. Create cache key from request
        cache_params = {
            'region': request.region,
            'year': request.year,
            'rainfall_delta': request.rainfall_delta,
            'temperature_delta': request.temperature_delta,
            'urban_growth': request.urban_growth
        }
        
        # 3. Check cache first
        cached_result = self.cache.get(cache_params)
        if cached_result:
            # Reconstruct nested models from cached dict
            if isinstance(cached_result.get('stats'), dict):
                cached_result['stats'] = SimulationStats(**cached_result['stats'])
            if isinstance(cached_result.get('results'), dict):
                cached_result['results'] = SimulationResults(**cached_result['results'])
            return SimulationResponse(**cached_result)
        
        # 4. Fetch baseline data (with fallback to mock)
        try:
            baseline_data = self.data_loader.fetch_baseline_state(
                request.region, 
                year=2020  # Use fixed baseline year
            )
            data_source = "real"
        except Exception as e:
            # Fallback to mock data if GEE fails
            error_msg = str(e)
            if "not registered" in error_msg.lower() or "earth engine" in error_msg.lower():
                baseline_data = self._get_mock_baseline(request.region)
                data_source = "mock"
            else:
                raise HTTPException(
                    status_code=500,
                    detail=f"Failed to fetch baseline data: {str(e)}"
                )
        
        # 5. Prepare scenario parameters
        scenario = {
            'target_year': request.year,
            'rainfall_delta': request.rainfall_delta,
            'temperature_delta': request.temperature_delta,
            'urban_growth': request.urban_growth
        }
        
        # 6. Run simulation
        import time
        start_time = time.time()
        
        try:
            results = self.simulation_engine.run_simulation(baseline_data, scenario)
        except Exception as e:
            import traceback
            print(f"SIMULATION ENGINE ERROR: {str(e)}")
            traceback.print_exc()
            raise HTTPException(
                status_code=500,
                detail=f"Simulation failed: {str(e)}"
            )
        
        computation_time = time.time() - start_time
        
        # 7. Build response
        response_data = {
            'scenario_id': results['scenario_id'],
            'metadata': results['metadata'],
            'results': SimulationResults(
                climate_stress=results.get('climate_stress', {}),
                land_transitions=results.get('land_transitions', {})
            ),
            'stats': SimulationStats(
                urban_gain_pct=results['summary_stats'].get('urban_gain_pct', 0),
                vegetation_loss_pct=results['summary_stats'].get('vegetation_loss_pct', 0),
                crop_stress_index=results['summary_stats'].get('crop_stress_index', 0),
                trees_change_pct=results['summary_stats'].get('trees_change_pct', 0),
                crops_change_pct=results['summary_stats'].get('crops_change_pct', 0),
                overall_stress_level=results['summary_stats'].get('overall_stress_level', 'unknown'),
                cached=False,
                computation_time_seconds=round(computation_time, 2)
            ),
            'tile_url': results['tile_url'],
            'data_source': data_source
        }
        
        # 8. Cache the result (mark as cached for future retrievals)
        # Serialize to dict for caching
        stats_dict = response_data['stats'].model_dump() if hasattr(response_data['stats'], 'model_dump') else response_data['stats']
        stats_dict['cached'] = True  # Mark as cached for future retrievals
        
        cached_response = {
            'scenario_id': response_data['scenario_id'],
            'metadata': response_data['metadata'],
            'results': response_data['results'].model_dump() if hasattr(response_data['results'], 'model_dump') else response_data['results'],
            'stats': stats_dict,
            'tile_url': response_data['tile_url'],
            'data_source': response_data['data_source']
        }
        self.cache.set(cache_params, cached_response)
        
        return SimulationResponse(**response_data)
    
    def _get_mock_baseline(self, region: str) -> Dict[str, Any]:
        """
        Generate mock baseline data for testing
        
        Args:
            region: Region name
            
        Returns:
            Mock baseline data structure
        """
        # Import regions to get bounding box
        from app.utils.regions import REGIONS, _normalize_region_name
        
        normalized_name = _normalize_region_name(region)
        region_data = REGIONS.get(normalized_name, {})
        
        return {
            'region': region,
            'year': 2020,
            'region_info': {
                'bounds': region_data.get('bbox', [77.0, 10.0, 80.0, 13.0]),  # Default Tamil Nadu bbox
                'name': normalized_name
            },
            'land_cover': {
                'classes': {
                    '1': 500,   # trees
                    '2': 300,   # grass
                    '4': 700,   # crops
                    '5': 200,   # shrub
                    '6': 200,   # built
                    '7': 100    # bare
                },
                'metadata': {'note': 'Mock data - GEE not available'}
            },
            'rainfall': {'annual_mean_mm': 1000},
            'temperature': {'mean_celsius': 25.0},
            'ndvi': {'mean_ndvi': 0.55}
        }

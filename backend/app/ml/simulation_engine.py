"""
Simulation Engine
Orchestrates the complete alternate Earth future simulation

Combines:
- Real baseline data (from GEE)
- Climate stress model
- Land transition model
- Scenario parameters

Produces: Alternate future Earth state
"""
import hashlib
import json
import numpy as np
from typing import Dict, Optional
from datetime import datetime

from app.ml.climate_stress import ClimateStressModel
from app.ml.land_transition import LandTransitionModel


class SimulationEngine:
    """
    Core simulation engine that generates alternate Earth futures
    
    This is NOT prediction - it's scenario-based simulation.
    """
    
    def __init__(self):
        """Initialize models"""
        self.climate_model = ClimateStressModel()
        self.land_model = LandTransitionModel()
    
    def generate_scenario_id(self, scenario_params: Dict) -> str:
        """
        Generate unique ID for a scenario
        
        Args:
            scenario_params: Scenario configuration
            
        Returns:
            Unique scenario ID (hash of parameters)
        """
        # Sort keys for consistent hashing
        param_str = json.dumps(scenario_params, sort_keys=True)
        hash_obj = hashlib.md5(param_str.encode())
        return hash_obj.hexdigest()[:12]
    
    def run_simulation(
        self,
        baseline_data: Dict,
        scenario: Dict
    ) -> Dict:
        """
        Run complete simulation
        
        Args:
            baseline_data: Real Earth data from GEE
                {
                    'region': 'Tamil Nadu',
                    'year': 2020,
                    'land_cover': {...},
                    'rainfall': {...},
                    'temperature': {...},
                    'ndvi': {...}
                }
            
            scenario: Future scenario parameters
                {
                    'target_year': 2035,
                    'rainfall_delta': -15,      # % change
                    'temperature_delta': 1.2,   # °C change
                    'urban_growth': 30          # % growth
                }
        
        Returns:
            Complete simulation results
        """
        # Generate scenario ID
        scenario_id = self.generate_scenario_id({
            'region': baseline_data['region'],
            'year': baseline_data['year'],
            'scenario': scenario
        })
        
        # Step 1: Calculate climate stress
        baseline_ndvi = baseline_data.get('ndvi', {}).get('mean_ndvi', 0.5)
        
        climate_stress = self.climate_model.calculate_combined_stress(
            rainfall_delta=scenario.get('rainfall_delta', 0),
            temp_delta=scenario.get('temperature_delta', 0),
            baseline_ndvi=baseline_ndvi
        )
        
        # Step 2: Prepare baseline land cover distribution
        land_cover_data = baseline_data.get('land_cover', {})
        baseline_distribution = self._prepare_land_cover_distribution(land_cover_data)
        
        # Step 3: Simulate land transitions
        land_transitions = self.land_model.calculate_stress_transitions(
            baseline_distribution=baseline_distribution,
            vegetation_stress=climate_stress['vegetation_stress_index'],
            urban_growth_pct=scenario.get('urban_growth', 0)
        )
        
        # Step 4: Calculate additional metrics
        metrics = self._calculate_additional_metrics(
            baseline_data,
            climate_stress,
            land_transitions,
            scenario
        )
        
        # Step 5: Assemble results
        # Calculate area-based metrics for land transitions
        # Estimate region area from bounding box (rough approximation)
        region_info = baseline_data.get('region_info', {})
        bounds = region_info.get('bounds', [0, 0, 1, 1])
        
        # Rough area calculation: degrees to km (1 degree ≈ 111 km at equator)
        # This uses lat/lon degrees, accounting for Earth's curvature
        width_km = abs(bounds[2] - bounds[0]) * 111 * abs(np.cos(np.radians((bounds[1] + bounds[3]) / 2)))
        height_km = abs(bounds[3] - bounds[1]) * 111
        total_area_km2 = width_km * height_km
        
        # Calculate degraded and urbanized areas
        summary = land_transitions.get('summary', {})
        baseline = land_transitions.get('baseline', {})
        future = land_transitions.get('future', {})
        
        # Urbanized area: increase in built-up land (in percentage points)
        baseline_built = baseline.get('built', 0)
        future_built = future.get('built', 0)
        urbanization_increase_pct = max(0, future_built - baseline_built)
        urbanized_area_km2 = (urbanization_increase_pct / 100) * total_area_km2
        
        # Degraded area: loss in productive vegetation (trees, crops, grass)
        # This is ADDITIONAL to urbanization - represents climate/stress damage
        # We need to calculate what was lost beyond what urbanization took
        baseline_vegetation = baseline.get('trees', 0) + baseline.get('crops', 0) + baseline.get('grass', 0)
        future_vegetation = future.get('trees', 0) + future.get('crops', 0) + future.get('grass', 0)
        total_veg_loss_pct = max(0, baseline_vegetation - future_vegetation)
        
        # Subtract urbanization from vegetation loss to get pure degradation
        # (Urbanization takes vegetation, but that's not "degradation")
        degradation_pct = max(0, total_veg_loss_pct - urbanization_increase_pct)
        degraded_area_km2 = (degradation_pct / 100) * total_area_km2
        
        results = {
            'scenario_id': scenario_id,
            'metadata': {
                'region': baseline_data['region'],
                'baseline_year': baseline_data['year'],
                'target_year': scenario.get('target_year', baseline_data['year'] + 15),
                'generated_at': datetime.utcnow().isoformat()
            },
            'scenario_inputs': scenario,
            'climate_stress': climate_stress,
            'land_cover': {
                'baseline': land_transitions['baseline'],
                'future': land_transitions['future'],
                'transitions': land_transitions['transitions']
            },
            'land_transitions': {
                'degraded_area_km2': round(degraded_area_km2, 2),
                'urbanized_area_km2': round(urbanized_area_km2, 2),
                'total_area_km2': round(total_area_km2, 2)
            },
            'summary_stats': {
                **land_transitions['summary'],
                **metrics
            },
            'tile_url': f"/tiles/{scenario_id}/{{z}}/{{x}}/{{y}}.png"
        }
        
        return results
    
    def _prepare_land_cover_distribution(self, land_cover_data: Dict) -> Dict[str, float]:
        """
        Convert GEE land cover data to percentage distribution
        
        Args:
            land_cover_data: Land cover data from GEE
            
        Returns:
            Distribution dict (e.g., {'trees': 30.5, 'crops': 25.0, ...})
        """
        classes = land_cover_data.get('classes', {})
        
        if not classes:
            # Return default distribution if no data
            return {
                'trees': 20.0,
                'grass': 15.0,
                'crops': 30.0,
                'shrub': 10.0,
                'built': 10.0,
                'bare': 10.0,
                'water': 5.0
            }
        
        # Convert class counts to percentages
        # Dynamic World classes mapping
        class_map = {
            '0': 'water',
            '1': 'trees',
            '2': 'grass',
            '3': 'flooded_vegetation',
            '4': 'crops',
            '5': 'shrub',
            '6': 'built',
            '7': 'bare',
            '8': 'snow'
        }
        
        # Calculate total
        total = sum(float(v) for v in classes.values())
        
        # Convert to percentages
        distribution = {}
        for class_id, count in classes.items():
            class_name = class_map.get(str(class_id), f'class_{class_id}')
            percentage = (float(count) / total * 100) if total > 0 else 0
            distribution[class_name] = round(percentage, 2)
        
        return distribution
    
    def _calculate_additional_metrics(
        self,
        baseline_data: Dict,
        climate_stress: Dict,
        land_transitions: Dict,
        scenario: Dict
    ) -> Dict:
        """Calculate additional summary metrics"""
        
        # Get key stats
        baseline_rainfall = baseline_data.get('rainfall', {}).get('annual_mean_mm', 1000)
        baseline_temp = baseline_data.get('temperature', {}).get('mean_celsius', 25)
        
        # Calculate future values
        future_rainfall = baseline_rainfall * (1 + scenario.get('rainfall_delta', 0) / 100)
        future_temp = baseline_temp + scenario.get('temperature_delta', 0)
        
        # Urban expansion metrics
        baseline_built = land_transitions['baseline'].get('built', 0)
        future_built = land_transitions['future'].get('built', 0)
        urban_gain = future_built - baseline_built
        
        return {
            'baseline_rainfall_mm': round(baseline_rainfall, 1),
            'future_rainfall_mm': round(future_rainfall, 1),
            'baseline_temp_celsius': round(baseline_temp, 1),
            'future_temp_celsius': round(future_temp, 1),
            'urban_area_baseline_pct': round(baseline_built, 2),
            'urban_area_future_pct': round(future_built, 2),
            'urban_gain_pct': round(urban_gain, 2),
            'crop_stress_index': climate_stress['vegetation_stress_index'],
            'overall_stress_level': climate_stress['crop_stress_level']
        }
    
    def get_scenario_summary(self, results: Dict) -> str:
        """
        Generate human-readable summary of scenario
        
        Args:
            results: Simulation results
            
        Returns:
            Summary text
        """
        metadata = results['metadata']
        stats = results['summary_stats']
        stress = results['climate_stress']
        
        summary = f"""
ALTERNATE EARTH FUTURE SCENARIO
Region: {metadata['region']}
Timeline: {metadata['baseline_year']} → {metadata['target_year']}

CLIMATE CHANGES:
- Rainfall: {stats.get('baseline_rainfall_mm', 0):.0f} → {stats.get('future_rainfall_mm', 0):.0f} mm/year
- Temperature: {stats.get('baseline_temp_celsius', 0):.1f} → {stats.get('future_temp_celsius', 0):.1f} °C

STRESS ASSESSMENT:
- Vegetation Stress: {stress['vegetation_stress_index']:.2f} / 1.0
- Crop Stress Level: {stress['crop_stress_level'].upper()}

LAND COVER IMPACTS:
- Vegetation Loss: {stats.get('vegetation_loss_pct', 0):.1f}%
- Urban Expansion: {stats.get('urban_gain_pct', 0):.1f}%
- Tree Cover Change: {stats.get('trees_change_pct', 0):.1f}%
- Crop Area Change: {stats.get('crops_change_pct', 0):.1f}%

NOTE: This is a SIMULATION, not a prediction.
It shows one possible future under specified conditions.
""".strip()
        
        return summary


# Convenience function
def simulate_scenario(baseline_data: Dict, scenario: Dict) -> Dict:
    """
    Quick function to run a simulation
    
    Args:
        baseline_data: Baseline Earth data from GEE
        scenario: Scenario parameters
        
    Returns:
        Simulation results
    """
    engine = SimulationEngine()
    return engine.run_simulation(baseline_data, scenario)

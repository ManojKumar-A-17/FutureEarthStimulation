"""
Climate Stress Model
Calculates vegetation and crop stress based on climate change deltas

This is SIMULATION logic, not prediction.
Simple, deterministic, explainable thresholds.
"""
import numpy as np
from typing import Dict, Tuple


class ClimateStressModel:
    """
    Calculates stress on vegetation and crops due to climate changes
    
    Philosophy:
    - Uses simple thresholds based on agronomic research
    - Deterministic (same input → same output)
    - Explainable (no black box)
    """
    
    def __init__(self):
        """Initialize stress thresholds"""
        # Rainfall stress thresholds (% change)
        self.rainfall_thresholds = {
            'severe_drought': -30,  # >30% decrease
            'moderate_drought': -15,
            'mild_drought': -5,
            'normal': 0,
            'excess': 20
        }
        
        # Temperature stress thresholds (°C change)
        self.temp_thresholds = {
            'extreme_heat': 2.0,   # >2°C increase
            'high_heat': 1.5,
            'moderate_heat': 1.0,
            'mild_heat': 0.5,
            'normal': 0
        }
        
        # NDVI health thresholds
        self.ndvi_thresholds = {
            'healthy': 0.6,
            'moderate': 0.4,
            'stressed': 0.2,
            'barren': 0.1
        }
    
    def calculate_rainfall_stress(self, rainfall_delta: float) -> float:
        """
        Calculate stress factor from rainfall change
        
        Args:
            rainfall_delta: % change in rainfall (-100 to +100)
            
        Returns:
            Stress factor (0.0 = no stress, 1.0 = maximum stress)
        """
        if rainfall_delta >= 0:
            # Excess rainfall (less stressful than drought)
            stress = min(rainfall_delta / 50.0, 0.5)  # Cap at 0.5
        else:
            # Drought conditions
            stress = min(abs(rainfall_delta) / 30.0, 1.0)  # Normalize to 0-1
        
        return stress
    
    def calculate_temperature_stress(self, temp_delta: float) -> float:
        """
        Calculate stress factor from temperature change
        
        Args:
            temp_delta: Temperature change in °C
            
        Returns:
            Stress factor (0.0 = no stress, 1.0 = maximum stress)
        """
        if temp_delta <= 0:
            # Cooling is generally less stressful
            return 0.0
        
        # Warming stress (normalized)
        stress = min(temp_delta / 3.0, 1.0)  # 3°C = max stress
        return stress
    
    def calculate_combined_stress(
        self, 
        rainfall_delta: float,
        temp_delta: float,
        baseline_ndvi: float = 0.5
    ) -> Dict:
        """
        Calculate combined climate stress index
        
        Args:
            rainfall_delta: % change in rainfall
            temp_delta: Change in temperature (°C)
            baseline_ndvi: Current vegetation health (0-1)
            
        Returns:
            Dictionary with stress metrics
        """
        # Individual stress components
        rainfall_stress = self.calculate_rainfall_stress(rainfall_delta)
        temp_stress = self.calculate_temperature_stress(temp_delta)
        
        # Combined stress (weighted average)
        # Rainfall is typically more critical for vegetation
        combined_stress = (rainfall_stress * 0.6) + (temp_stress * 0.4)
        
        # Adjust based on baseline NDVI (healthier vegetation more resilient)
        resilience_factor = baseline_ndvi  # Higher NDVI = more resilient
        adjusted_stress = combined_stress * (1.0 - resilience_factor * 0.3)
        
        # Vegetation impact (0 = no impact, 1 = severe impact)
        vegetation_stress_index = np.clip(adjusted_stress, 0.0, 1.0)
        
        # Classify crop stress level
        if adjusted_stress >= 0.7:
            crop_stress_level = "severe"
        elif adjusted_stress >= 0.5:
            crop_stress_level = "high"
        elif adjusted_stress >= 0.3:
            crop_stress_level = "moderate"
        elif adjusted_stress >= 0.1:
            crop_stress_level = "mild"
        else:
            crop_stress_level = "low"
        
        return {
            'vegetation_stress_index': float(vegetation_stress_index),
            'crop_stress_level': crop_stress_level,
            'components': {
                'rainfall_stress': float(rainfall_stress),
                'temperature_stress': float(temp_stress),
                'combined_stress': float(combined_stress)
            },
            'inputs': {
                'rainfall_delta_pct': rainfall_delta,
                'temp_delta_celsius': temp_delta,
                'baseline_ndvi': baseline_ndvi
            }
        }
    
    def estimate_vegetation_loss(
        self,
        stress_index: float,
        current_vegetation_area: float
    ) -> float:
        """
        Estimate vegetation area loss based on stress
        
        Args:
            stress_index: Vegetation stress index (0-1)
            current_vegetation_area: Current vegetation area (any unit)
            
        Returns:
            Estimated vegetation loss (same unit as input)
        """
        # Loss percentage based on stress
        # Stress 0.0 → 0% loss
        # Stress 0.5 → ~15% loss
        # Stress 1.0 → ~40% loss (not 100%, some vegetation survives)
        
        loss_factor = stress_index * 0.4  # Max 40% loss
        vegetation_loss = current_vegetation_area * loss_factor
        
        return vegetation_loss
    
    def get_stress_explanation(self, stress_data: Dict) -> str:
        """
        Generate human-readable explanation of stress factors
        
        Args:
            stress_data: Output from calculate_combined_stress()
            
        Returns:
            Explanation string
        """
        inputs = stress_data['inputs']
        level = stress_data['crop_stress_level']
        
        explanation = f"Climate stress level: {level.upper()}\n"
        
        if inputs['rainfall_delta_pct'] < -20:
            explanation += "⚠️ Severe drought conditions detected\n"
        elif inputs['rainfall_delta_pct'] < -10:
            explanation += "⚠️ Moderate drought conditions\n"
        
        if inputs['temp_delta_celsius'] > 2.0:
            explanation += "⚠️ Extreme temperature increase\n"
        elif inputs['temp_delta_celsius'] > 1.0:
            explanation += "⚠️ Significant warming detected\n"
        
        return explanation


# Convenience function
def calculate_climate_stress(
    rainfall_delta: float,
    temp_delta: float,
    baseline_ndvi: float = 0.5
) -> Dict:
    """
    Quick function to calculate climate stress
    
    Args:
        rainfall_delta: % change in rainfall
        temp_delta: Temperature change in °C
        baseline_ndvi: Baseline vegetation health (0-1)
        
    Returns:
        Climate stress metrics
    """
    model = ClimateStressModel()
    return model.calculate_combined_stress(rainfall_delta, temp_delta, baseline_ndvi)

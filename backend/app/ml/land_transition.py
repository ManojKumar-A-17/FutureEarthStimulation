"""
Land Transition Model
Simulates how land cover classes change under stress and development pressure

This is SIMULATION, not prediction.
Rule-based transitions with explainable logic.
"""
import numpy as np
from typing import Dict, List, Tuple


class LandTransitionModel:
    """
    Models transitions between land cover classes
    
    Dynamic World Classes:
    0: Water
    1: Trees (forest)
    2: Grass
    3: Flooded vegetation
    4: Crops
    5: Shrub and scrub
    6: Built (urban)
    7: Bare ground
    8: Snow and ice
    """
    
    def __init__(self):
        """Initialize transition rules and class names"""
        self.class_names = {
            0: 'water',
            1: 'trees',
            2: 'grass',
            3: 'flooded_vegetation',
            4: 'crops',
            5: 'shrub',
            6: 'built',
            7: 'bare',
            8: 'snow'
        }
        
        # Base transition probabilities (stress = 0, urban growth = 0)
        # These represent natural, slow changes
        self.base_transitions = self._define_base_transitions()
    
    def _define_base_transitions(self) -> Dict:
        """
        Define base transition probabilities
        
        Format: {from_class: {to_class: probability}}
        """
        return {
            1: {1: 0.95, 2: 0.03, 5: 0.02},  # Trees mostly stable
            2: {2: 0.90, 5: 0.05, 7: 0.05},  # Grass can degrade
            4: {4: 0.85, 2: 0.10, 7: 0.05},  # Crops can fail
            5: {5: 0.90, 2: 0.05, 7: 0.05},  # Shrub semi-stable
            7: {7: 0.95, 2: 0.03, 5: 0.02},  # Bare mostly stays bare
        }
    
    def calculate_stress_transitions(
        self,
        baseline_distribution: Dict[str, float],
        vegetation_stress: float,
        urban_growth_pct: float = 0.0
    ) -> Dict:
        """
        Calculate land cover transitions under stress and development
        
        Args:
            baseline_distribution: Current land cover % (e.g., {'trees': 30, 'crops': 40})
            vegetation_stress: Stress index (0-1)
            urban_growth_pct: Urban area increase % (0-100)
            
        Returns:
            Future land cover distribution with transition details
        """
        # Convert to working dict
        current = {k: float(v) for k, v in baseline_distribution.items()}
        future = current.copy()
        transitions = {}
        
        # 1. Apply stress-based degradation
        if vegetation_stress > 0.01:
            stress_transitions = self._apply_stress_degradation(
                current, vegetation_stress
            )
            future = stress_transitions['future']
            transitions['stress'] = stress_transitions['changes']
        
        # 2. Apply urban expansion
        if urban_growth_pct > 0:
            urban_transitions = self._apply_urban_expansion(
                future, urban_growth_pct
            )
            future = urban_transitions['future']
            transitions['urbanization'] = urban_transitions['changes']
        
        # 3. Normalize to 100%
        total = sum(future.values())
        if total > 0:
            future = {k: (v / total) * 100 for k, v in future.items()}
        
        return {
            'baseline': baseline_distribution,
            'future': future,
            'transitions': transitions,
            'summary': self._calculate_summary_stats(current, future)
        }
    
    def _apply_stress_degradation(
        self,
        current: Dict[str, float],
        stress: float
    ) -> Dict:
        """
        Apply vegetation stress to land cover
        
        High stress causes:
        - Trees → Grass/Shrub
        - Crops → Bare
        - Grass → Bare
        """
        future = current.copy()
        changes = {}
        
        # Stress factor (0 = no change, 1 = maximum degradation)
        degradation_rate = stress * 0.1  # Max 10% of area can degrade (Dampened from 30%)
        
        # Trees degradation
        if 'trees' in future and future['trees'] > 0:
            trees_loss = future['trees'] * degradation_rate
            future['trees'] -= trees_loss
            
            # Trees become grass (60%) or shrub (40%)
            grass_gain = trees_loss * 0.6
            shrub_gain = trees_loss * 0.4
            
            future['grass'] = future.get('grass', 0) + grass_gain
            future['shrub'] = future.get('shrub', 0) + shrub_gain
            
            changes['trees_to_grass'] = grass_gain
            changes['trees_to_shrub'] = shrub_gain
        
        # Crops failure
        if 'crops' in future and future['crops'] > 0:
            # Crops more sensitive to stress
            crop_loss = future['crops'] * (degradation_rate * 1.5)
            crop_loss = min(crop_loss, future['crops'])
            future['crops'] -= crop_loss
            
            # Failed crops become grass (40%) or bare (60%)
            grass_gain = crop_loss * 0.4
            bare_gain = crop_loss * 0.6
            
            future['grass'] = future.get('grass', 0) + grass_gain
            future['bare'] = future.get('bare', 0) + bare_gain
            
            changes['crops_to_grass'] = grass_gain
            changes['crops_to_bare'] = bare_gain
        
        # Grass degradation
        if 'grass' in future and future['grass'] > 0:
            grass_loss = future['grass'] * degradation_rate * 0.5
            future['grass'] -= grass_loss
            future['bare'] = future.get('bare', 0) + grass_loss
            
            changes['grass_to_bare'] = grass_loss
        
        return {'future': future, 'changes': changes}
    
    def _apply_urban_expansion(
        self,
        current: Dict[str, float],
        growth_pct: float
    ) -> Dict:
        """
        Apply urban expansion
        
        Urban growth takes from:
        - Crops (primary target)
        - Grass (secondary)
        - Trees (tertiary)
        """
        future = current.copy()
        changes = {}
        
        # Calculate new urban area
        current_built = future.get('built', 0)
        
        # Ensure minimum base for growth (if built < 1%, assume 1% as base for expansion simulation)
        # This allows new settlements to form in rural areas
        base_built = max(current_built, 1.0)
        
        new_built_area = base_built * (growth_pct / 100.0)
        
        # Urban expansion takes from available land in priority order
        remaining_needed = new_built_area
        
        # Priority 1: Crops
        if 'crops' in future and future['crops'] > 0 and remaining_needed > 0:
            take_from_crops = min(remaining_needed, future['crops'] * 0.4)  # Max 40%
            future['crops'] -= take_from_crops
            remaining_needed -= take_from_crops
            changes['crops_to_built'] = take_from_crops
        
        # Priority 2: Grass
        if 'grass' in future and future['grass'] > 0 and remaining_needed > 0:
            take_from_grass = min(remaining_needed, future['grass'] * 0.3)
            future['grass'] -= take_from_grass
            remaining_needed -= take_from_grass
            changes['grass_to_built'] = take_from_grass
        
        # Priority 3: Trees
        if 'trees' in future and future['trees'] > 0 and remaining_needed > 0:
            take_from_trees = min(remaining_needed, future['trees'] * 0.2)
            future['trees'] -= take_from_trees
            remaining_needed -= take_from_trees
            changes['trees_to_built'] = take_from_trees
        
        # Add to built area
        future['built'] = current_built + (new_built_area - remaining_needed)
        
        return {'future': future, 'changes': changes}
    
    def _calculate_summary_stats(
        self,
        baseline: Dict[str, float],
        future: Dict[str, float]
    ) -> Dict:
        """Calculate summary statistics of transitions"""
        stats = {}
        
        # Calculate changes for key classes
        for class_name in ['built', 'trees', 'crops', 'grass', 'bare']:
            baseline_val = baseline.get(class_name, 0)
            future_val = future.get(class_name, 0)
            
            change = future_val - baseline_val
            change_pct = (change / baseline_val * 100) if baseline_val > 0 else 0
            
            stats[f'{class_name}_change_pct'] = round(change_pct, 2)
        
        # Calculate vegetation loss (trees + crops + grass)
        veg_classes = ['trees', 'crops', 'grass', 'shrub']
        baseline_veg = sum(baseline.get(c, 0) for c in veg_classes)
        future_veg = sum(future.get(c, 0) for c in veg_classes)
        
        if baseline_veg > 0:
            veg_loss_pct = ((baseline_veg - future_veg) / baseline_veg) * 100
            stats['vegetation_loss_pct'] = round(veg_loss_pct, 2)
        
        return stats


# Convenience function
def simulate_land_transitions(
    baseline_distribution: Dict[str, float],
    vegetation_stress: float,
    urban_growth_pct: float = 0.0
) -> Dict:
    """
    Quick function to simulate land cover transitions
    
    Args:
        baseline_distribution: Current land cover percentages
        vegetation_stress: Stress index (0-1)
        urban_growth_pct: Urban growth percentage
        
    Returns:
        Transition results with future distribution
    """
    model = LandTransitionModel()
    return model.calculate_stress_transitions(
        baseline_distribution,
        vegetation_stress,
        urban_growth_pct
    )

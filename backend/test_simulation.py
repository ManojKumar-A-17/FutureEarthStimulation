"""
Test script for simulation engine (without Earth Engine)
Tests the ML models with mock data
"""
from app.ml.climate_stress import calculate_climate_stress
from app.ml.land_transition import simulate_land_transitions
from app.ml.simulation_engine import SimulationEngine
import json


def test_climate_stress():
    """Test climate stress calculation"""
    print("=" * 60)
    print("TEST 1: Climate Stress Model")
    print("=" * 60)
    
    # Scenario: Moderate drought + warming
    result = calculate_climate_stress(
        rainfall_delta=-15.0,  # 15% decrease
        temp_delta=1.2,        # 1.2°C increase
        baseline_ndvi=0.5
    )
    
    print(json.dumps(result, indent=2))
    print()


def test_land_transitions():
    """Test land transition model"""
    print("=" * 60)
    print("TEST 2: Land Transition Model")
    print("=" * 60)
    
    # Mock baseline distribution
    baseline = {
        'trees': 25.0,
        'crops': 35.0,
        'grass': 15.0,
        'shrub': 10.0,
        'built': 10.0,
        'bare': 5.0
    }
    
    result = simulate_land_transitions(
        baseline_distribution=baseline,
        vegetation_stress=0.6,  # Moderate-high stress
        urban_growth_pct=30.0   # 30% urban growth
    )
    
    print("Baseline Distribution:")
    print(json.dumps(result['baseline'], indent=2))
    print("\nFuture Distribution:")
    print(json.dumps(result['future'], indent=2))
    print("\nSummary Stats:")
    print(json.dumps(result['summary'], indent=2))
    print()


def test_full_simulation():
    """Test complete simulation engine"""
    print("=" * 60)
    print("TEST 3: Complete Simulation Engine")
    print("=" * 60)
    
    # Mock baseline data (simulating GEE data)
    baseline_data = {
        'region': 'Test Region',
        'year': 2020,
        'land_cover': {
            'classes': {
                '1': 500,   # trees
                '2': 300,   # grass
                '4': 700,   # crops
                '5': 200,   # shrub
                '6': 200,   # built
                '7': 100    # bare
            }
        },
        'rainfall': {'annual_mean_mm': 1000},
        'temperature': {'mean_celsius': 25.0},
        'ndvi': {'mean_ndvi': 0.55}
    }
    
    # Scenario
    scenario = {
        'target_year': 2035,
        'rainfall_delta': -20.0,  # 20% decrease (severe drought)
        'temperature_delta': 1.5,  # 1.5°C warming
        'urban_growth': 40.0       # 40% urban expansion
    }
    
    # Run simulation
    engine = SimulationEngine()
    results = engine.run_simulation(baseline_data, scenario)
    
    # Print summary
    print(engine.get_scenario_summary(results))
    print("\n" + "=" * 60)
    print("Full Results:")
    print(json.dumps(results, indent=2))
    print()


if __name__ == "__main__":
    print("\n🚀 TESTING SIMULATION ENGINE\n")
    
    test_climate_stress()
    test_land_transitions()
    test_full_simulation()
    
    print("=" * 60)
    print("✅ ALL TESTS COMPLETED")
    print("=" * 60)

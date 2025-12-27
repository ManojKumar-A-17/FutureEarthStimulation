"""
Verify simulation calculations
"""
import requests
import json

def test_simulation(region, rainfall, temp, urban_growth):
    """Test a simulation scenario"""
    url = "http://localhost:8000/simulate"
    payload = {
        "region": region,
        "rainfall_delta": rainfall,
        "temperature_delta": temp,
        "urban_growth": urban_growth
    }
    
    response = requests.post(url, json=payload)
    data = response.json()
    
    print(f"\n{'='*70}")
    print(f"SCENARIO: {region.upper()}")
    print(f"Rainfall: {rainfall}%, Temperature: {temp}°C, Urban Growth: {urban_growth}%")
    print(f"{'='*70}")
    
    # Metadata
    meta = data['metadata']
    print(f"\nRegion: {meta['region']}")
    print(f"Baseline Year: {meta['baseline_year']} → Target Year: {meta['target_year']}")
    
    # Stats
    stats = data['stats']
    print(f"\n📊 STATISTICS:")
    print(f"  Urban Gain: {stats['urban_gain_pct']}%")
    print(f"  Vegetation Loss: {stats['vegetation_loss_pct']}%")
    print(f"  Crop Stress Index: {stats['crop_stress_index']}")
    print(f"  Trees Change: {stats['trees_change_pct']}%")
    print(f"  Crops Change: {stats['crops_change_pct']}%")
    print(f"  Overall Stress: {stats['overall_stress_level']}")
    
    # Land Transitions
    lt = data['results']['land_transitions']
    print(f"\n🌍 LAND TRANSITIONS:")
    print(f"  Total Area: {lt['total_area_km2']:,.2f} km²")
    print(f"  Degraded Area: {lt['degraded_area_km2']:,.2f} km²")
    print(f"  Urbanized Area: {lt['urbanized_area_km2']:,.2f} km²")
    print(f"  % Degraded: {(lt['degraded_area_km2']/lt['total_area_km2']*100):.2f}%")
    print(f"  % Urbanized: {(lt['urbanized_area_km2']/lt['total_area_km2']*100):.2f}%")
    
    # Climate Stress
    cs = data['results']['climate_stress']
    print(f"\n🌡️ CLIMATE STRESS:")
    print(f"  Vegetation Stress Index: {cs['vegetation_stress_index']}")
    print(f"  Crop Stress Level: {cs['crop_stress_level']}")
    print(f"  Rainfall Stress: {cs['components']['rainfall_stress']}")
    print(f"  Temperature Stress: {cs['components']['temperature_stress']}")
    print(f"  Combined Stress: {cs['components']['combined_stress']}")
    
    return data

if __name__ == "__main__":
    print("Testing Simulation Calculations...")
    
    # Test 1: No changes (baseline)
    print("\n\n" + "="*70)
    print("TEST 1: BASELINE (No Changes)")
    print("="*70)
    test_simulation("tamilnadu", 0, 0, 0)
    
    # Test 2: Only urban growth
    print("\n\n" + "="*70)
    print("TEST 2: URBAN GROWTH ONLY")
    print("="*70)
    test_simulation("tamilnadu", 0, 0, 60)
    
    # Test 3: Climate stress only
    print("\n\n" + "="*70)
    print("TEST 3: CLIMATE STRESS ONLY")
    print("="*70)
    test_simulation("tamilnadu", -30, 2, 0)
    
    # Test 4: Combined scenario
    print("\n\n" + "="*70)
    print("TEST 4: COMBINED SCENARIO")
    print("="*70)
    test_simulation("tamilnadu", -20, 1.5, 40)
    
    print("\n\n" + "="*70)
    print("VERIFICATION COMPLETE")
    print("="*70)

"""
Test distance calculator functionality
"""

import sys
import os
import logging

# Setup logging to see INFO messages
logging.basicConfig(level=logging.INFO, format='%(message)s')

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.utils.distance_calculator import (
    calculate_distance_miles,
    is_within_commute_range,
    geocode_location,
    clear_geocode_cache
)


def test_geocoding():
    """Test basic geocoding functionality with smart city/county selection"""
    print("\n" + "="*70)
    print("TEST 1: Geocoding Accuracy")
    print("="*70)
    
    # Clear cache for fresh test
    clear_geocode_cache()
    
    # Test that Wayne, PA returns the town (not Wayne County)
    coords_wayne = geocode_location("Wayne, PA")
    print(f"Wayne, PA: {coords_wayne}")
    assert coords_wayne is not None, "Failed to geocode Wayne, PA"
    # Wayne town is around (40.04, -75.39), Wayne County is around (41.6, -75.3)
    assert 39.5 < coords_wayne[0] < 40.5, f"Wayne geocoded to wrong location (got {coords_wayne[0]}° lat, expected ~40°)"
    
    # Test other cities
    coords_philly = geocode_location("Philadelphia, PA")
    coords_wc = geocode_location("West Chester, PA")
    coords_malvern = geocode_location("Malvern, PA")
    
    print(f"Philadelphia, PA: {coords_philly}")
    print(f"West Chester, PA: {coords_wc}")
    print(f"Malvern, PA: {coords_malvern}")
    
    assert coords_philly is not None, "Failed to geocode Philadelphia"
    assert coords_wc is not None, "Failed to geocode West Chester"
    assert coords_malvern is not None, "Failed to geocode Malvern"
    
    print("✅ All locations geocoded successfully\n")


def test_distance_calculation():
    """Test distance calculation between cities"""
    print("="*70)
    print("TEST 2: Distance Calculations")
    print("="*70)
    
    # West Chester to Wayne (should be ~13-15 miles)
    distance = calculate_distance_miles("West Chester, PA", "Wayne, PA")
    print(f"West Chester, PA → Wayne, PA: {distance:.1f} miles")
    assert distance is not None, "Failed to calculate distance"
    assert 10 <= distance <= 20, f"Expected ~13 miles, got {distance:.1f}"
    
    # Philadelphia to Malvern (should be ~18-22 miles)
    distance = calculate_distance_miles("Philadelphia, PA", "Malvern, PA")
    print(f"Philadelphia, PA → Malvern, PA: {distance:.1f} miles")
    assert 15 <= distance <= 25, f"Expected ~20 miles, got {distance:.1f}"
    
    # Philadelphia to New York (should be ~80-90 miles)
    distance = calculate_distance_miles("Philadelphia, PA", "New York, NY")
    print(f"Philadelphia, PA → New York, NY: {distance:.1f} miles")
    assert 75 <= distance <= 95, f"Expected ~80 miles, got {distance:.1f}"
    
    print("✅ All distance calculations passed\n")


def test_commute_range():
    """Test commute range checking"""
    print("="*70)
    print("TEST 3: Commute Range Checking")
    print("="*70)
    
    # Test within range
    is_acceptable, distance, reason = is_within_commute_range(
        job_location="Malvern, PA",
        candidate_location="West Chester, PA",
        max_commute_miles=50
    )
    print(f"West Chester to Malvern (50 mile max):")
    print(f"  Acceptable: {is_acceptable}, Distance: {distance}, Reason: {reason}")
    assert is_acceptable, "Should be within 50 mile range"
    
    # Test outside range
    is_acceptable, distance, reason = is_within_commute_range(
        job_location="New York, NY",
        candidate_location="Philadelphia, PA",
        max_commute_miles=50
    )
    print(f"\nPhiladelphia to NYC (50 mile max):")
    print(f"  Acceptable: {is_acceptable}, Distance: {distance}, Reason: {reason}")
    assert not is_acceptable, "Should be outside 50 mile range"
    
    # Test with target cities exception
    is_acceptable, distance, reason = is_within_commute_range(
        job_location="New York, NY",
        candidate_location="Philadelphia, PA",
        max_commute_miles=20,
        acceptable_long_commute_cities=["New York, NY", "Boston, MA"]
    )
    print(f"\nPhiladelphia to NYC (20 mile max, but NYC in target cities):")
    print(f"  Acceptable: {is_acceptable}, Distance: {distance}, Reason: {reason}")
    assert is_acceptable, "Should be acceptable due to target cities list"
    
    print("✅ All commute range checks passed\n")


if __name__ == "__main__":
    print("\n" + "="*70)
    print("DISTANCE CALCULATOR TEST SUITE")
    print("="*70)
    
    try:
        test_geocoding()
        test_distance_calculation()
        test_commute_range()
        
        print("="*70)
        print("✅ ALL TESTS PASSED!")
        print("="*70 + "\n")
        sys.exit(0)
        
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}\n")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

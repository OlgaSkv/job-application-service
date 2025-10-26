"""
Distance calculator utility using GeoPy for location-based eligibility checks.

Uses OpenStreetMap's Nominatim geocoding service (free, no API key required).
Includes caching to minimize API calls and respect rate limits.
"""

import logging
from typing import Optional, Tuple, Dict
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
import time

# Cache for geocoded locations to minimize API calls
_geocode_cache: Dict[str, Tuple[float, float]] = {}

# Initialize geolocator (required user agent for Nominatim)
geolocator = Nominatim(user_agent="job-tracker-app", timeout=10)


def _score_geocode_result(result) -> int:
    """
    Score a geocode result to prefer cities/towns over counties.

    Returns higher score for more specific locations (cities, towns with postcodes)
    and lower/negative scores for vague locations (counties).
    """
    score = 0
    address = result.raw.get("address", {})
    display_name = result.raw.get("display_name", "")
    result_type = result.raw.get("type", "")
    result_class = result.raw.get("class", "")

    # Prefer places (cities, towns, villages)
    if result_class == "place":
        score += 100

    # Prefer specific settlement types
    if result_type in ["city", "town", "village", "borough", "hamlet"]:
        score += 50
    elif result_type in ["suburb", "neighbourhood"]:
        score += 30

    # Prefer results with postcodes (more specific)
    if "postcode" in address:
        score += 40

    # Penalize county-level results (too vague)
    if result_type == "administrative" and "county" in display_name.lower():
        score -= 100

    return score


def geocode_location(location: str) -> Optional[Tuple[float, float]]:
    """
    Convert location string to coordinates (latitude, longitude).

    Uses smart scoring to prefer cities/towns over counties (e.g., "Wayne, PA"
    returns Wayne town in Delaware County, not Wayne County).

    Args:
        location: Location string like "Philadelphia, PA" or "New York, NY"

    Returns:
        (latitude, longitude) tuple or None if geocoding fails
    """
    if not location or not location.strip():
        return None

    location = location.strip()

    # Check cache first
    if location in _geocode_cache:
        logging.debug(f"Using cached coordinates for: {location}")
        return _geocode_cache[location]

    try:
        # Respect Nominatim rate limit (1 req/sec)
        time.sleep(1.1)

        # Add ", USA" for US state abbreviations (PA, NY, etc.)
        query = location
        if ", USA" not in location.upper() and ", US" not in location.upper():
            parts = location.split(",")
            if len(parts) >= 2 and len(parts[-1].strip()) == 2 and parts[-1].strip().isupper():
                query = f"{location}, USA"

        # Get multiple results to pick the best one
        results = geolocator.geocode(
            query, exactly_one=False, country_codes="us", addressdetails=True, limit=5
        )

        if not results:
            logging.warning(f"Could not geocode location: {location}")
            return None

        # Score results and pick the best one
        best_result = max(results, key=_score_geocode_result, default=results[0])

        coords = (best_result.latitude, best_result.longitude)
        _geocode_cache[location] = coords

        # logging.info(f"Geocoded '{location}' -> {coords}")
        return coords

    except (GeocoderTimedOut, GeocoderServiceError) as e:
        logging.error(f"Geocoding error for '{location}': {e}")
        return None
    except Exception as e:
        logging.error(f"Unexpected geocoding error for '{location}': {e}")
        return None


def calculate_distance_miles(location1: str, location2: str) -> Optional[float]:
    """
    Calculate distance in miles between two locations.

    Args:
        location1: First location (e.g., "Philadelphia, PA")
        location2: Second location (e.g., "New York, NY")

    Returns:
        Distance in miles, or None if geocoding fails
    """
    coords1 = geocode_location(location1)
    coords2 = geocode_location(location2)

    if not coords1 or not coords2:
        logging.warning(f"Cannot calculate distance between '{location1}' and '{location2}'")
        return None

    try:
        distance = geodesic(coords1, coords2).miles
        logging.info(f"Distance: {location1} → {location2} = {distance:.1f} miles")
        return distance
    except Exception as e:
        logging.error(f"Error calculating distance: {e}")
        return None


def is_within_commute_range(
    job_location: str,
    candidate_location: str,
    max_commute_miles: int,
    acceptable_long_commute_cities: list = None,
) -> Tuple[bool, Optional[float], str]:
    """
    Check if job location is within acceptable commute distance.

    Args:
        job_location: Job location string
        candidate_location: Candidate's current location
        max_commute_miles: Maximum acceptable commute distance in miles
        acceptable_long_commute_cities: Cities where distance check is waived

    Returns:
        Tuple of (is_acceptable, distance_miles, reason_message)
    """
    acceptable_long_commute_cities = acceptable_long_commute_cities or []

    # Check if job location matches a target city (skip distance check)
    # Use intelligent matching that handles variations like "New York, NY" vs "New York City, NY"
    for city in acceptable_long_commute_cities:
        if not city or not job_location:
            continue
            
        city_lower = city.lower()
        job_location_lower = job_location.lower()
        
        # Direct substring match
        if city_lower in job_location_lower:
            return True, None, f"Job location matches target city: {city}"
        
        # Extract city name and state (e.g., "New York" from "New York, NY")
        # Handle formats: "City, ST" or "City Name, ST"
        if "," in city_lower:
            city_name = city_lower.split(",")[0].strip()
            # Check if the city name appears in the job location
            # This handles "New York, NY" matching "New York City, NY"
            if city_name in job_location_lower and city_lower.split(",")[1].strip() in job_location_lower:
                return True, None, f"Job location matches target city: {city}"

    # Calculate actual distance
    distance = calculate_distance_miles(job_location, candidate_location)

    if distance is None:
        return False, None, f"Could not calculate distance to '{job_location}'"

    # Check against max commute threshold
    if distance <= max_commute_miles:
        return True, distance, f"Within commute range: {distance:.1f} miles"
    else:
        return False, distance, f"Too far: {distance:.1f} miles (max: {max_commute_miles})"


def clear_geocode_cache():
    """Clear the geocoding cache. Useful for testing."""
    global _geocode_cache
    _geocode_cache.clear()
    logging.info("Geocode cache cleared")

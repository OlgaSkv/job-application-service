"""
config_utils.py - Centralized configuration loading with caching

Provides a simple get_config() function to load config.json once and cache it.
"""

import json

# Global cache for config.json to avoid repeated file reads
_config_cache = None


def get_config():
    """Load and cache configuration from config.json."""
    global _config_cache

    if _config_cache is None:
        with open("config.json", "r", encoding="utf-8") as f:
            _config_cache = json.load(f)

    return _config_cache

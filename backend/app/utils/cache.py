"""
In-memory caching system for scenarios
Prevents redundant computation and GEE API calls
"""
from typing import Dict, Any, Optional
from datetime import datetime, timedelta
import hashlib
import json


class ScenarioCache:
    """
    Simple in-memory cache for simulation scenarios
    
    Features:
    - Hash-based lookup
    - TTL (time-to-live) support
    - Memory efficient (stores only stats, not full rasters)
    """
    
    def __init__(self, max_size: int = 100, ttl_hours: int = 24):
        """
        Initialize cache
        
        Args:
            max_size: Maximum number of cached scenarios
            ttl_hours: Time-to-live in hours
        """
        self._cache: Dict[str, Dict[str, Any]] = {}
        self.max_size = max_size
        self.ttl = timedelta(hours=ttl_hours)
    
    def _generate_key(self, params: Dict[str, Any]) -> str:
        """
        Generate cache key from parameters
        
        Args:
            params: Scenario parameters
            
        Returns:
            Hash string as cache key
        """
        # Sort keys for consistent hashing
        param_str = json.dumps(params, sort_keys=True)
        return hashlib.md5(param_str.encode()).hexdigest()[:12]
    
    def get(self, params: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Get cached scenario if available and not expired
        
        Args:
            params: Scenario parameters
            
        Returns:
            Cached data or None
        """
        key = self._generate_key(params)
        
        if key not in self._cache:
            return None
        
        cached = self._cache[key]
        
        # Check if expired
        if datetime.utcnow() - cached['cached_at'] > self.ttl:
            # Remove expired entry
            del self._cache[key]
            return None
        
        # Update last accessed time
        cached['last_accessed'] = datetime.utcnow()
        return cached['data']
    
    def set(self, params: Dict[str, Any], data: Dict[str, Any]) -> str:
        """
        Store scenario in cache
        
        Args:
            params: Scenario parameters
            data: Simulation results to cache
            
        Returns:
            Cache key (scenario_id)
        """
        key = self._generate_key(params)
        
        # Enforce max size (simple FIFO)
        if len(self._cache) >= self.max_size:
            # Remove oldest entry
            oldest_key = min(
                self._cache.keys(),
                key=lambda k: self._cache[k].get('cached_at', datetime.min)
            )
            del self._cache[oldest_key]
        
        # Store with metadata
        self._cache[key] = {
            'data': data,
            'cached_at': datetime.utcnow(),
            'last_accessed': datetime.utcnow(),
            'params': params
        }
        
        return key
    
    def clear(self):
        """Clear all cached scenarios"""
        self._cache.clear()
    
    def size(self) -> int:
        """Get current cache size"""
        return len(self._cache)
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        return {
            'size': len(self._cache),
            'max_size': self.max_size,
            'ttl_hours': self.ttl.total_seconds() / 3600,
            'cached_scenarios': list(self._cache.keys())
        }


# Global cache instance
_scenario_cache = ScenarioCache()


def get_cache() -> ScenarioCache:
    """Get global cache instance"""
    return _scenario_cache


def clear_cache():
    """Clear global cache"""
    _scenario_cache.clear()

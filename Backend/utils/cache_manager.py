"""
Redis Cache Manager for Vehicle Parking Management System
Provides caching functionality with expiry, invalidation, and performance optimization
"""

import json
import redis
import functools
import logging
from datetime import datetime, timedelta
from typing import Any, Optional, Union, Dict, List
from flask import current_app, request, g
import hashlib

logger = logging.getLogger(__name__)

class CacheManager:
    """Redis-based cache manager with decorators and utility methods"""
    
    def __init__(self, app=None):
        self.redis_client = None
        if app:
            self.init_app(app)
    
    def init_app(self, app):
        """Initialize cache with Flask app"""
        try:
            self.redis_client = redis.Redis.from_url(
                app.config.get('REDIS_CACHE_URL', 'redis://localhost:6379/1'),
                decode_responses=True
            )
            # Test connection
            self.redis_client.ping()
            app.extensions['cache'] = self
            logger.info("Redis cache initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Redis cache: {e}")
            self.redis_client = None
    
    def _generate_cache_key(self, prefix: str, *args, **kwargs) -> str:
        """Generate a unique cache key"""
        key_parts = [prefix]
        
        # Add positional arguments
        for arg in args:
            if isinstance(arg, (dict, list)):
                key_parts.append(hashlib.md5(json.dumps(arg, sort_keys=True).encode()).hexdigest())
            else:
                key_parts.append(str(arg))
        
        # Add keyword arguments
        if kwargs:
            key_parts.append(hashlib.md5(json.dumps(kwargs, sort_keys=True).encode()).hexdigest())
        
        return ":".join(key_parts)
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        if not self.redis_client:
            return None
        
        try:
            value = self.redis_client.get(key)
            if value:
                return json.loads(value)
        except Exception as e:
            logger.error(f"Cache get error for key {key}: {e}")
        return None
    
    def set(self, key: str, value: Any, expiry: int = None) -> bool:
        """Set value in cache with optional expiry"""
        if not self.redis_client:
            return False
        
        try:
            serialized_value = json.dumps(value, default=str)
            if expiry:
                return self.redis_client.setex(key, expiry, serialized_value)
            else:
                return self.redis_client.set(key, serialized_value)
        except Exception as e:
            logger.error(f"Cache set error for key {key}: {e}")
            return False
    
    def delete(self, key: str) -> bool:
        """Delete key from cache"""
        if not self.redis_client:
            return False
        
        try:
            return bool(self.redis_client.delete(key))
        except Exception as e:
            logger.error(f"Cache delete error for key {key}: {e}")
            return False
    
    def delete_pattern(self, pattern: str) -> int:
        """Delete all keys matching pattern"""
        if not self.redis_client:
            return 0
        
        try:
            keys = self.redis_client.keys(pattern)
            if keys:
                return self.redis_client.delete(*keys)
            return 0
        except Exception as e:
            logger.error(f"Cache delete pattern error for {pattern}: {e}")
            return 0
    
    def invalidate_user_cache(self, user_id: int):
        """Invalidate all cache entries for a specific user"""
        patterns = [
            f"user_profile:{user_id}:*",
            f"user_reservations:{user_id}:*",
            f"user_dashboard:{user_id}:*"
        ]
        for pattern in patterns:
            self.delete_pattern(pattern)
    
    def invalidate_parking_cache(self, lot_id: int = None):
        """Invalidate parking-related cache"""
        if lot_id:
            patterns = [
                f"parking_lots:{lot_id}:*",
                f"parking_spots:{lot_id}:*",
                "parking_lots:all:*"
            ]
        else:
            patterns = [
                "parking_lots:*",
                "parking_spots:*",
                "dashboard_stats:*"
            ]
        
        for pattern in patterns:
            self.delete_pattern(pattern)

# Cache decorators
def cached_response(cache_key_prefix: str, expiry_config_key: str = None, expiry_seconds: int = 300):
    """
    Decorator for caching API responses
    
    Args:
        cache_key_prefix: Prefix for cache key
        expiry_config_key: Key in CACHE_EXPIRY config
        expiry_seconds: Default expiry in seconds
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            cache = current_app.extensions.get('cache')
            if not cache:
                return func(*args, **kwargs)
            
            # Generate cache key
            cache_key = cache._generate_cache_key(
                cache_key_prefix,
                *args,
                **kwargs,
                user_id=getattr(g, 'user_id', None)
            )
            
            # Try to get from cache
            cached_result = cache.get(cache_key)
            if cached_result:
                logger.debug(f"Cache hit for key: {cache_key}")
                return cached_result
            
            # Execute function
            result = func(*args, **kwargs)
            
            # Cache successful responses
            if hasattr(result, 'status_code') and result.status_code == 200:
                expiry = current_app.config.get('CACHE_EXPIRY', {}).get(expiry_config_key, expiry_seconds)
                cache.set(cache_key, result.get_json(), expiry)
                logger.debug(f"Cached result for key: {cache_key}")
            
            return result
        return wrapper
    return decorator

def cached_query(cache_key_prefix: str, expiry_seconds: int = 300):
    """
    Decorator for caching database query results
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            cache = current_app.extensions.get('cache')
            if not cache:
                return func(*args, **kwargs)
            
            # Generate cache key
            cache_key = cache._generate_cache_key(cache_key_prefix, *args, **kwargs)
            
            # Try to get from cache
            cached_result = cache.get(cache_key)
            if cached_result:
                logger.debug(f"Query cache hit for key: {cache_key}")
                return cached_result
            
            # Execute query
            result = func(*args, **kwargs)
            
            # Cache result
            if result is not None:
                cache.set(cache_key, result, expiry_seconds)
                logger.debug(f"Cached query result for key: {cache_key}")
            
            return result
        return wrapper
    return decorator

# Initialize cache manager
cache_manager = CacheManager()
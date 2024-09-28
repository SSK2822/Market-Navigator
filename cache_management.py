import redis
import json

# Initialize Redis connection
r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

def cache_data(key, data):
    """
    Caches data in Redis under a given key.

    Args:
    key (str): The Redis key under which to store the data.
    data (dict): The data to cache.

    Note: Converts data to a JSON string before caching.
    """
    r.set(key, json.dumps(data))

def get_cached_data(key):
    """
    Retrieves cached data from Redis under a given key.

    Args:
    key (str): The Redis key from which to fetch the data.

    Returns:
    dict or None: The cached data if available, or None.
    """
    cached_data = r.get(key)
    return json.loads(cached_data) if cached_data else None

def clear_cache(key):
    """
    Clears cached data from Redis under a given key.

    Args:
    key (str): The Redis key to clear.
    """
    r.delete(key)

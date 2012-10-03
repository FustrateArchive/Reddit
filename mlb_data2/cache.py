"""
Caching
"""

import memcache, pickle

cache = memcache.Client(["127.0.0.1:11211"], debug=0)
cache_hits = 0
cache_misses = []

def load(key):
	data = cache.get(key)
	
	if data is not None:
		cache_hits += 1
		return data[0] if not data[1] else pickle.loads(data[0])
	
	cache_misses.append(key)

def save(key, data, ttl):
	pickled = False

	if isinstance(data, object):
		data = pickle.dumps(data, 2)
		pickled = True

	cache.delete(key)
	cache.add(key, [data, pickled], time.time() + ttl)
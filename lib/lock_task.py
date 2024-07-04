import json


DEFAULT_LOCK_TIME = 86400000 # 1 days

class LockTaskHelper:

    def __init__(self, lock_key, redis, lock_ttl=DEFAULT_LOCK_TIME) -> None:
        self.lock_key = lock_key
        self.redis = redis

        if not DEFAULT_LOCK_TIME:
            lock_ttl = int(DEFAULT_LOCK_TIME)
        self.lock_ttl = lock_ttl

    def get_key(self, key_suffix):
        return f'{self.lock_key}:{key_suffix}'

    def is_lock(self, key_suffix):
        _key = self.get_key(key_suffix=key_suffix)
        _existed = self.redis.exists(_key)
        if not _existed:
            return False

        return True

    def lock(self, key_suffix):
        _key = self.get_key(key_suffix=key_suffix)
        self.redis.setex(_key, self.lock_ttl, 'lock')

    def unlock(self, key_suffix):
        _key = self.get_key(key_suffix=key_suffix)
        self.redis.delete(_key)
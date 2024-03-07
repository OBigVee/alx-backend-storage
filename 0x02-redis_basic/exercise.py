#!/usr/bin/env python3
"""Write strings to Redis"""

import redis
from uuid import uuid4
from typing import Optional, Union


class Cache:
    """class"""

    def __init__(self) -> None:
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]):
        """method generates a random key and stores the input
        data in Redis using the random key and return the key
        """
        key = str(uuid4())
        self._redis.mset({key: data})

        return key

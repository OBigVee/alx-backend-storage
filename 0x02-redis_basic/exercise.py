#!/usr/bin/env python3
"""Write strings to Redis"""

import redis
from uuid import uuid4
from typing import Optional, Union, Callable
from functools import wraps


def count_calls(m: Callable) -> Callable:
    """returns callable"""
    mKey = m.__qualname__

    @wraps(m)
    def wrapper(self, *args, **kwds):
        """
        Wrapper function
        function increments the count for mKey everytime mkey
        mKey method is called.
        return: Counts
        """
        self._redis.incr(mKey)
        return m(self, *args, **kwds)

    # return the value returned in  count_call method
    return wrapper


class Cache:
    """class"""

    def __init__(self) -> None:
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """method generates a random key and stores the input
        data in Redis using the random key and return the key
        """
        key = str(uuid4())
        self._redis.mset({key: data})

        return key

    def get(self, key: str, fn: Optional[Callable]) -> Union[str, bytes, int, float]:
        """returns data of a key in a decoded form.

        key: str
        fn: Callable argument
        """
        data = self._redis.get(key)

        # conserve Redis.get behaviour if key does not exit
        if fn is not None:
            return fn(data)
        return data

    def get_str(self, data: str) -> str:
        """decode byte to str"""
        return data.decode("utf-8")

    def get_int(self, data: str) -> int:
        """decode byte to int"""
        return int(data)

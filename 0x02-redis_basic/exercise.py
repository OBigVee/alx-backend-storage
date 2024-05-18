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
    def wrapper(self, *args, **kwargs):
        """
        Wrapper function
        function increments the count for mKey everytime mkey
        mKey method is called.
        return: Counts
        """
        self._redis.incr(mKey)
        return m(self, *args, **kwargs)

    # return the value returned in  count_call method
    return wrapper


def call_history(m: Callable) -> Callable:
    """decorator stores the history of inputs for a particular
    function"""

    # mKey = m.__qualname__
    # inputs = mKey + ":inputs"
    # outputs = mKey + ":outputs"

    @wraps(m)
    def wrapper(self, *args, **kwargs):
        """_summary_"""
        input = str(args)
        # self._redis.rpush(inputs, input)
        # output = str(m(self, *args, **kwargs))
        # self._redis.rpush(outputs, output)
        self._redis.rpush(m.__qualname__ + ":inputs", input)
        output = str(m(self, *args, **kwargs))
        self._redis.rpush(m.__qualname__ + ":outputs", output)

    return wrapper


class Cache:
    """class"""

    def __init__(self) -> None:
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """method generates a random key and stores the input
        data in Redis using the random key and return the key
        """
        key = str(uuid4())
        self._redis.mset({key: data})

        return key

    def get(
        self,
        key: str,
        fn: Optional[Callable] = None) -> Union[
            str,
            bytes,
            int, float]:
        """returns data of a key in a decoded form.

        key: str
        fn: Callable argument
        """
        data = self._redis.get(key)

        # conserve Redis.get behaviour if key does not exit
        if fn:
            data = fn(data)
        return data

    def get_str(self, data: str) -> str:
        """decode byte to str"""
        data = self._redis.get(data)
        return data.decode("utf-8")

    def get_int(self, data: str) -> int:
        """decode byte to int"""
        data = self._redis.get(data)
        try:
            data = int(data.decode("utf-8"))
        except Exception:
            data = 0
        return data

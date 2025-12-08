# Utility functions
from functools import lru_cache

@lru_cache(maxsize=128)
def expensive_operation(x):
    return x ** 2

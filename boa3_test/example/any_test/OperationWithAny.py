from typing import Any


def Main():
    a: Any = 5
    b = 3 + a  # compiler error - cannot use any when expecting a typed value

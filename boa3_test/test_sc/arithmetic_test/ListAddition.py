from typing import Any

from boa3.sc.compiletime import public


@public
def add_any(a: list[Any], b: list[Any]) -> list[Any]:
    return a + b


@public
def add_int(a: list[int], b: list[int]) -> list[int]:
    return a + b


@public
def add_bool(a: list[bool], b: list[bool]) -> list[bool]:
    return a + b


@public
def add_str(a: list[str], b: list[str]) -> list[str]:
    return a + b

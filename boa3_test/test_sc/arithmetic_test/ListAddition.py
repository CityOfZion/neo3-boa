from typing import Any, List

from boa3.builtin.compile_time import public


@public
def add_any(a: List[Any], b: List[Any]) -> List[Any]:
    return a + b


@public
def add_int(a: List[int], b: List[int]) -> List[int]:
    return a + b


@public
def add_bool(a: List[bool], b: List[bool]) -> List[bool]:
    return a + b


@public
def add_str(a: List[str], b: List[str]) -> List[str]:
    return a + b

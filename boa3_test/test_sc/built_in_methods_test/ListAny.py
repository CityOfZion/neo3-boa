from typing import Any, Union

from boa3.builtin.compile_time import public


@public
def main(x: Any) -> list[Any]:
    return list(x)


def verify_union_types_1(x: Union[int, str, bytes]) -> list[int]:
    return list(x)


def verify_union_types_2(x: Union[int, str]) -> list[str]:
    return list(x)


def verify_union_types_3(x: Union[list[int], str]) -> list[Union[str, int]]:
    return list(x)


def verify_union_types_4(x: Union[list[int], str]) -> list[Union[int, str]]:
    return list(x)


def verify_union_types_5(x: Union[dict[str, bytes], int]) -> list[str]:
    return list(x)


def verify_union_types_6(x: Union[dict[str, bytes], list[bytes], str, bytes]) -> list[str, int, bytes]:
    return list(x)

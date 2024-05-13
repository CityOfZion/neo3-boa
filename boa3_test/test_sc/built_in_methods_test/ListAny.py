from typing import Any

from boa3.sc.compiletime import public


@public
def main(x: Any) -> list[Any]:
    return list(x)


def verify_union_types_1(x: int | str | bytes) -> list[int]:
    return list(x)


def verify_union_types_2(x: int | str) -> list[str]:
    return list(x)


def verify_union_types_3(x: list[int] | str) -> list[str | int]:
    return list(x)


def verify_union_types_4(x: list[int] | str) -> list[int | str]:
    return list(x)


def verify_union_types_5(x: dict[str, bytes] | int) -> list[str]:
    return list(x)


def verify_union_types_6(x: dict[str, bytes] | list[bytes] | str | bytes) -> list[str, int, bytes]:
    return list(x)

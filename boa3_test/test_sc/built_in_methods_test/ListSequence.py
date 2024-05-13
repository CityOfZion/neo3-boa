from collections.abc import Sequence
from typing import Any

from boa3.sc.compiletime import public


@public
def main(x: Sequence) -> list[Any]:
    return list(x)


@public
def verify_list_unchanged(x: list[Any]) -> list[Any]:
    new_list = list(x)

    x[0] = x[1]

    return new_list


def verify_return_type_int() -> list[int]:
    return list([123, 45, 512, 1265, 76134, 121])


def verify_return_type_str() -> list[str]:
    return list(['unit', 'test', 'aaa', ''])


def verify_return_type_bytes() -> list[bytes]:
    return list([b'unit', b'test', b'aaa', b''])

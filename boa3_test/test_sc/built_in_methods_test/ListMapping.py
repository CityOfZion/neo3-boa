from typing import Any, Mapping

from boa3.builtin.compile_time import public


@public
def main(x: Mapping) -> list[Any]:
    return list(x)


def verify_return_type_int() -> list[int]:
    return list(
        {1: '123', 2: '4', 45: '123', 123: '00'}
    )


def verify_return_type_str() -> list[str]:
    return list(
        {'1': 123, '2': '4', '45': '123', '123': 00}
    )


def verify_return_type_bytes() -> list[bytes]:
    return list(
        {b'1': 123, b'2': '4', b'45': '123', b'123': 00}
    )

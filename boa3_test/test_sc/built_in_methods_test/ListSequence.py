from typing import Any, List, Sequence

from boa3.builtin.compile_time import public


@public
def main(x: Sequence) -> List[Any]:
    return list(x)


@public
def verify_list_unchanged(x: List[Any]) -> List[Any]:
    new_list = list(x)

    x[0] = x[1]

    return new_list


def verify_return_type_int() -> List[int]:
    return list([123, 45, 512, 1265, 76134, 121])


def verify_return_type_str() -> List[str]:
    return list(['unit', 'test', 'aaa', ''])


def verify_return_type_bytes() -> List[bytes]:
    return list([b'unit', b'test', b'aaa', b''])

from typing import Any, Dict, List, Union

from boa3.builtin.compile_time import public


@public
def main(x: Any) -> List[Any]:
    return list(x)


def verify_union_types_1(x: Union[int, str, bytes]) -> List[int]:
    return list(x)


def verify_union_types_2(x: Union[int, str]) -> List[str]:
    return list(x)


def verify_union_types_3(x: Union[List[int], str]) -> List[Union[str, int]]:
    return list(x)


def verify_union_types_4(x: Union[List[int], str]) -> List[Union[int, str]]:
    return list(x)


def verify_union_types_5(x: Union[Dict[str, bytes], int]) -> List[str]:
    return list(x)


def verify_union_types_6(x: Union[Dict[str, bytes], List[bytes], str, bytes]) -> List[str, int, bytes]:
    return list(x)

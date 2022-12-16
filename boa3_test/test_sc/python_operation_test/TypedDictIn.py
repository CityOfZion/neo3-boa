from typing import Dict

from boa3.builtin.compile_time import public


@public
def main(value: int, some_dict: Dict[int, str]) -> bool:
    return value in some_dict

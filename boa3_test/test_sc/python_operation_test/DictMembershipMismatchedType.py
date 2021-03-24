from typing import Dict

from boa3.builtin import public


@public
def main(value: int, some_dict: Dict[str, int]) -> bool:
    return value in some_dict

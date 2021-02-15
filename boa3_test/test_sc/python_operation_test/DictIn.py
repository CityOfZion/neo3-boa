from typing import Any

from boa3.builtin import public


@public
def main(value: Any, some_dict: dict) -> bool:
    return value in some_dict

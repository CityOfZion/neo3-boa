from typing import Any

from boa3.sc.compiletime import public


@public
def main(value: Any, some_dict: dict) -> bool:
    return value not in some_dict

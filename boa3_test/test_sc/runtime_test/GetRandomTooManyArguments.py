from typing import Any

from boa3.sc.runtime import get_random


def main(arg: Any) -> int:
    return get_random(arg)

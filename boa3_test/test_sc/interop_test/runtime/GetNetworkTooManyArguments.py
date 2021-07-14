from typing import Any

from boa3.builtin.interop.runtime import get_network


def main(arg: Any) -> int:
    return get_network(arg)

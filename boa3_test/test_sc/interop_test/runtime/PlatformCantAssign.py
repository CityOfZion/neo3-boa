from boa3.builtin import public
from boa3.builtin.interop.runtime import platform


@public
def main(example: str) -> str:
    platform = example
    return platform


def interop_call():
    x = platform

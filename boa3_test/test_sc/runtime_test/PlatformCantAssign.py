from boa3.sc.compiletime import public
from boa3.sc.runtime import platform


@public
def main(example: str) -> str:
    platform = example
    return platform


def interop_call():
    x = platform

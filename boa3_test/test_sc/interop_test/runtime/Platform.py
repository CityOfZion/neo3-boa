from boa3.builtin import public
from boa3.builtin.interop.runtime import platform


@public
def main() -> str:
    return platform

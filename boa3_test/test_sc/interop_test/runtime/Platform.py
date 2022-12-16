from boa3.builtin.compile_time import public
from boa3.builtin.interop.runtime import platform


@public
def main() -> str:
    return platform

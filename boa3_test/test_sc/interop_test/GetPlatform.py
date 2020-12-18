from boa3.builtin import public
from boa3.builtin.interop.runtime import get_platform


@public
def main() -> str:
    return get_platform

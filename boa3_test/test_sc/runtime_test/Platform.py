from boa3.sc.compiletime import public
from boa3.sc.runtime import platform


@public
def main() -> str:
    return platform

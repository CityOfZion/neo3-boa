from boa3.sc.compiletime import public
from boa3.sc.contracts import StdLib
from boa3.sc.types import UInt160


@public
def main() -> UInt160:
    return StdLib.hash

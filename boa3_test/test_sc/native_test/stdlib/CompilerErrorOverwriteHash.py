from boa3.sc.contracts import StdLib
from boa3.sc.types import UInt160


def main() -> UInt160:
    StdLib.hash = UInt160()
    return StdLib.hash

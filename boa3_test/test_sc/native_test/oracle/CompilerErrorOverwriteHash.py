from boa3.sc.contracts import OracleContract
from boa3.sc.types import UInt160


def main() -> UInt160:
    OracleContract.hash = UInt160()
    return OracleContract.hash

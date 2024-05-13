from boa3.sc.compiletime import public
from boa3.sc.contracts import OracleContract


@public
def main() -> int:
    return OracleContract.get_price()

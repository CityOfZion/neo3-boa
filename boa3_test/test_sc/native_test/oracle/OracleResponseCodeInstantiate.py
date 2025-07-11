from boa3.sc.compiletime import public
from boa3.sc.types import OracleResponseCode


@public
def main(x: int) -> OracleResponseCode:
    return OracleResponseCode(x)

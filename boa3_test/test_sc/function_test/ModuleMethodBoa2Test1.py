from boa3.sc.compiletime import public
from boa3.sc.contracts import CryptoLib

MYSHA = CryptoLib.sha256('abc')


@public
def main() -> bool:

    m = 3

    j2 = CryptoLib.sha256('abc')

    j3 = MYSHA

    return j2 == j3

from boa3.sc.compiletime import public
from boa3.sc.types import NamedCurveHash


@public
def main(x: NamedCurveHash) -> int:
    return ~x

from boa3.sc.compiletime import public
from boa3.sc.types import FindOptions


@public
def main(x: FindOptions) -> FindOptions:
    return ~x

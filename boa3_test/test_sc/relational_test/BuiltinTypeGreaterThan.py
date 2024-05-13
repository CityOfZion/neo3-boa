from boa3.sc.compiletime import public
from boa3.sc.types import FindOptions


@public
def main(a: FindOptions, b: FindOptions) -> bool:
    return a > b

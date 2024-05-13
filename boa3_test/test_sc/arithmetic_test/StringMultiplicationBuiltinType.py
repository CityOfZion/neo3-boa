from boa3.sc.compiletime import public
from boa3.sc.types import FindOptions


@public
def str_mult(a: str, b: FindOptions) -> str:
    return a * b

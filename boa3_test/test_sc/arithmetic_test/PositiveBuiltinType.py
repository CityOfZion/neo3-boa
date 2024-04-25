from boa3.builtin.compile_time import public
from boa3.sc.types import FindOptions


@public
def plus(a: FindOptions) -> int:
    return +a

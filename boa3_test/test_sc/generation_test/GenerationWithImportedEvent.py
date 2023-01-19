from boa3.builtin.compile_time import public
from boa3_test.examples.nep17 import on_transfer


imported_transfer = on_transfer  # all events should be mapped in the manifest


@public
def Main(a: int, b: int) -> int:
    return a + b

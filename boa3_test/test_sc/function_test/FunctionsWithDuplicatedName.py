from boa3.sc.compiletime import public
from boa3.sc.types import UInt160


@public
def func_no_arg_with_return_array() -> list[int]:
    return [1, 2]


@public
def func_no_arg_with_return_array() -> list[UInt160]:
    return [UInt160(b'\x01' * 20), UInt160(b'\x02' * 20)]

from boa3.builtin import public
from boa3.builtin.type import UInt160
from typing import List


@public
def func_no_arg_with_return_array() -> List[int]:
    return [1, 2]


@public
def func_no_arg_with_return_array() -> List[UInt160]:
    return [UInt160(b'\x01' * 20), UInt160(b'\x02' * 20)]

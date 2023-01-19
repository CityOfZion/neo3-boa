from boa3.builtin.compile_time import public
from boa3.builtin.interop.runtime import calling_script_hash
from boa3.builtin.type import UInt160


@public
def Main(example: UInt160) -> UInt160:
    calling_script_hash = example
    return calling_script_hash


def interop_call():
    x = calling_script_hash

from typing import cast

from boa3.builtin.compile_time import public
from boa3.builtin.interop.contract import CallFlags
from boa3.builtin.interop.runtime import load_script
from boa3.builtin.vm import Opcode


@public
def dynamic_sum_with_flags(a: int, b: int, flags: CallFlags) -> int:
    script: bytes = Opcode.ADD
    return cast(int, load_script(script, [a, b], flags))


@public
def dynamic_sum(a: int, b: int) -> int:
    script: bytes = Opcode.ADD
    return cast(int, load_script(script, [a, b]))

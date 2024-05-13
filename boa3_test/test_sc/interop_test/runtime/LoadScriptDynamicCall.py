from typing import cast

from boa3.sc.compiletime import public
from boa3.sc.runtime import load_script
from boa3.sc.types import Opcode, CallFlags


@public
def dynamic_sum_with_flags(a: int, b: int, flags: CallFlags) -> int:
    script: bytes = Opcode.ADD
    return cast(int, load_script(script, [a, b], flags))


@public
def dynamic_sum(a: int, b: int) -> int:
    script: bytes = Opcode.ADD
    return cast(int, load_script(script, [a, b]))

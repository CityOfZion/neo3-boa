from boa3.builtin.compile_time import public
from boa3.builtin.type import UInt256
from boa3.builtin.interop.runtime import script_container


@public
def main() -> UInt256:
    return script_container.hash

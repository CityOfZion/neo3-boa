from boa3.builtin.compile_time import public
from boa3.builtin.type import UInt256
from boa3.builtin.interop import runtime

@public
def main() -> UInt256:
    return runtime.script_container.hash

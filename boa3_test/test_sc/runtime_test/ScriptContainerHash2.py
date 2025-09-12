from boa3.sc import runtime
from boa3.sc.compiletime import public
from boa3.sc.types import UInt256


@public
def main() -> UInt256:
    return runtime.script_container.hash

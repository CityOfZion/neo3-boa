from boa3.sc.compiletime import public
from boa3.sc.runtime import script_container
from boa3.sc.types import UInt256


@public
def main() -> UInt256:
    return script_container.hash

from boa3.builtin import interop
from boa3.sc.compiletime import public


@public
def main() -> int:
    return interop.runtime.get_trigger() + interop.runtime.get_trigger()

from boa3.builtin import public
from boa3.builtin.nativecontract.stdlib import StdLib


@public
def main() -> str:
    return StdLib.json_serialize(True)

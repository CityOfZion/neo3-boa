from boa3.builtin import public
from boa3.builtin.nativecontract.stdlib import StdLib


@public
def main() -> bytes:
    return StdLib.json_serialize(b'unit test')

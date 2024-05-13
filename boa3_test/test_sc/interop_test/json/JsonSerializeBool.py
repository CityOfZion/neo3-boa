from boa3.sc.compiletime import public
from boa3.sc.contracts import StdLib


@public
def main() -> str:
    return StdLib.json_serialize(True)

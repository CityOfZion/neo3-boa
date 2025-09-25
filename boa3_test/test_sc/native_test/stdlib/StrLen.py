from boa3.sc.compiletime import public
from boa3.sc.contracts import StdLib


@public
def main(string: str) -> int:
    return StdLib.str_len(string)

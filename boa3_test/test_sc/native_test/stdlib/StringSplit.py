from boa3.sc.compiletime import public
from boa3.sc.contracts import StdLib


@public
def main(string: str, separator: str) -> list[str]:
    return StdLib.string_split(string, separator)

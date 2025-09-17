from boa3.sc.compiletime import public
from boa3.sc.contracts import StdLib


@public
def main(string: str, separator: str, remove_empty_entries: bool) -> list[str]:
    return StdLib.string_split(string, separator, remove_empty_entries)

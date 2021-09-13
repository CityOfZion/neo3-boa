from boa3.builtin.nativecontract.stdlib import StdLib


def main() -> int:
    return StdLib.atoi('100', 10, 'extra')

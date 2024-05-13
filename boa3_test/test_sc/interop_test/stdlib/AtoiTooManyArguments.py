from boa3.sc.contracts import StdLib


def main() -> int:
    return StdLib.atoi('100', 10, 'extra')

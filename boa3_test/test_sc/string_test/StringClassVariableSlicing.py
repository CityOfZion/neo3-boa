from boa3.sc.compiletime import public


class Example:
    string = 'unit test'


@public
def main(start: int, end: int) -> str:
    return Example.string[start:end]

from boa3.builtin.compile_time import public


class Example:
    string = 'unit test'


@public
def main(start: int, end: int) -> str:
    return Example.string[start:end]

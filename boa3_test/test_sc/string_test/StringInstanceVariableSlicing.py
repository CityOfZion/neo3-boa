from boa3.builtin.compile_time import public


class Example:
    def __init__(self, string: str):
        self.string = string


@public
def main(string: str, start: int, end: int) -> str:
    obj = Example(string)
    return obj.string[start:end]

from boa3.sc.compiletime import public


class Example:
    def __init__(self, string: str):
        self.string = string


@public
def main(string: str, start: int, end: int) -> str:
    obj = Example(string)
    return obj.string[start:end]

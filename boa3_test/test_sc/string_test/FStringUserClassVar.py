from boa3.sc.compiletime import public


@public
def main() -> str:
    example_value = Example()
    fstring = f"F-string: {example_value}"
    return fstring


class Example:
    def __init__(self):
        self.string = 'unit test'
        self.number = 123

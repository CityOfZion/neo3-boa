from boa3.sc.compiletime import public


@public
def main() -> bool:
    return bool(Example())


class Example:
    def __init__(self):
        self.test = 123

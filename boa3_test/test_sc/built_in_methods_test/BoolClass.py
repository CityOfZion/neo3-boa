from boa3.builtin.compile_time import public


@public
def main() -> bool:
    return bool(Example())


class Example:
    def __init__(self):
        self.test = 123

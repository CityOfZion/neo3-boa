from boa3.builtin.compile_time import public


class Foo:
    def __init__(self, init_value: int):
        self.bar = init_value


class Example(Foo):
    def __init__(self):
        super().__init__(-10)


@public
def inherited_var() -> int:
    foo = Example()
    return foo.bar

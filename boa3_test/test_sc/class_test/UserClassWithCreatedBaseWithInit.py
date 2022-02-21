from boa3.builtin import public


class Foo:
    def __init__(self):
        self.bar = 42


class Example(Foo):
    def __init__(self):
        super().__init__()


@public
def inherited_var() -> int:
    foo = Example()
    return foo.bar

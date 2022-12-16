from boa3.builtin.compile_time import public


class Foo:
    def __init__(self):
        self.bar = 42


class Example(Foo):
    pass


@public
def implemented_variable() -> int:
    foo = Foo()
    return foo.bar


@public
def inherited_variable() -> int:
    foo = Example()
    return foo.bar


@public
def update_variable(new_value: int) -> int:
    foo = Example()
    foo.bar = new_value
    return foo.bar

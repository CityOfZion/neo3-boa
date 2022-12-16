from boa3.builtin.compile_time import public


class Foo:
    def __init__(self, init_value: int, other_arg: int):
        self.bar = init_value


class Example(Foo):
    pass


@public
def implemented_var(init_value: int) -> int:
    foo = Foo(init_value, 10)
    return foo.bar


@public
def inherited_var(init_value: int) -> int:
    foo = Example(init_value, 10)
    return foo.bar

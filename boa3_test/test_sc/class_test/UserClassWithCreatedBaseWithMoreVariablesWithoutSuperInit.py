from boa3.builtin.compile_time import public


class Foo:
    def __init__(self):
        self.bar = 42


class Example(Foo):
    def __init__(self):
        self.var_1 = 10
        self.var_2 = 20


@public
def get_full_object() -> Example:
    return Example()

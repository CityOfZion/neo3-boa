from boa3.builtin.compile_time import public


class Foo:
    def __init__(self, var_value: int):
        self.bar = var_value

    def test_method(self) -> int:
        return -20


class Example(Foo):
    def test_method(self) -> int:
        if self.bar > 30:
            return super(Example, self).test_method()  # super with args is not implemented yet
        return self.bar


@public
def example_method(var_value: int) -> int:
    foo = Example(var_value)
    return foo.test_method()

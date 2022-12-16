from boa3.builtin.compile_time import public


class Example:
    def __init__(self):
        self.val1 = 1
        self.val2 = 2

    def func(self, value1: int, value2: int) -> int:
        return self.val1 + self.val2 + value1 + value2


@public
def get_val() -> int:

    obj = Example()

    return Example.func(value2=10, value1=5, self=obj)

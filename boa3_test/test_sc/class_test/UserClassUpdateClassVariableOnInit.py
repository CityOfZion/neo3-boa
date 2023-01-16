from boa3.builtin.compile_time import public


class Example:
    class_val = 0

    def __init__(self):
        self.val1 = 1
        self.val2 = 2

        Example.class_val += 1


@public
def test_1(arg: int) -> Example:
    obj = Example()

    for _ in range(arg):
        Example()

    return obj


@public
def test_2(arg: int) -> Example:
    for _ in range(arg):
        Example()

    obj = Example()

    return obj

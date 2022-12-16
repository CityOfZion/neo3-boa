from boa3.builtin.compile_time import public


class Example:
    def __init__(self):
        self.val1 = 1
        self.val2 = 2


@public
def get_val1() -> int:
    example = Example()
    return example.val1


@public
def get_val2() -> int:
    example = Example()
    return example.val2

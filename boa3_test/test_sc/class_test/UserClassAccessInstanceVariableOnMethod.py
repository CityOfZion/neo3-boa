from boa3.builtin.compile_time import public


class Example:
    def __init__(self):
        self.val1 = 1
        self.val2 = 4

    def get_val1(self) -> int:
        return self.val1

    def get_val2(self) -> int:
        return self.val2


@public
def get_val1() -> int:
    return Example().get_val1()


@public
def get_val2() -> int:
    return Example().get_val2()

from boa3.sc.compiletime import public


class Example:
    def __init__(self):
        self.val1 = 1
        self.val2 = 2


@public
def get_val1() -> int:
    return Example.val1

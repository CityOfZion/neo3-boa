from boa3.builtin.compile_time import public


class Example:
    def __init__(self):
        self.val1 = 1
        self.val2 = 2


@public
def Main():
    example = Example()
    print(example)

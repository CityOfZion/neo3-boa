from boa3.builtin.compile_time import public


class Example:
    def __init__(self):
        self.val1 = 2
        self.val2 = self.val1 * 2


@public
def get_obj() -> Example:
    return Example()

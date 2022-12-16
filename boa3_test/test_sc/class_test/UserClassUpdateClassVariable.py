from boa3.builtin.compile_time import public


class Example:
    class_val = 10

    def __init__(self):
        self.val1 = 1
        self.val2 = 2


@public
def get_val(arg: int) -> Example:
    obj = Example()
    obj.class_val = arg
    return obj

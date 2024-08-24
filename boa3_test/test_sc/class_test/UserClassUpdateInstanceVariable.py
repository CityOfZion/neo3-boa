from boa3.sc.compiletime import public


class Example:
    class_val = 10

    def __init__(self):
        self.val1 = 1
        self.val2 = 2


@public
def get_val(arg: int) -> Example:
    obj = Example()
    obj.val1 = arg
    return obj

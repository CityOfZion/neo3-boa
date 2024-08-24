from boa3.sc.compiletime import public


class Example:
    def __init__(self):
        self.var_1 = 'example'

    def test(self) -> str:
        var_1 = 'example 2'
        if len(self.var_1) > 0:
            return self.var_1
        return var_1


@public
def main() -> str:
    var_1 = Example()

    return var_1.test()

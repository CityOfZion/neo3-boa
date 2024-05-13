from boa3.sc.compiletime import public


class Example:
    var_1 = 'example'

    @classmethod
    def test(cls) -> str:
        var_1 = 'example 2'
        if len(cls.var_1) > 0:
            return cls.var_1
        return var_1


@public
def main() -> str:
    a = Example()

    return a.test()

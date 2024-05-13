from boa3.sc.compiletime import public


class Example:
    @staticmethod
    def test() -> int:
        return 10


@public
def test() -> int:
    return 20


@public
def result() -> tuple[int, int]:
    a = Example.test()
    b = test()
    c = (a, b)
    return c

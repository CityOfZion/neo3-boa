from boa3.builtin.compile_time import public


class Example:
    def __init__(self):
        self._num = 1_000

    @property
    def number(self) -> int:
        return self._num


@public
def test() -> int:
    number = 10
    x = Example()
    return x.number

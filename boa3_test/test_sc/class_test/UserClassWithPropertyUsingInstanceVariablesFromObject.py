from boa3.builtin.compile_time import public


class Example:
    def __init__(self):
        self._ivar = 10

    @property
    def some_property(self) -> int:
        return self._ivar


@public
def get_property() -> int:
    return Example().some_property

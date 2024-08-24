from boa3.sc.compiletime import public


class Example:
    @property
    def some_property(self) -> int:
        x = 19
        y = 11
        z = 14
        return x + y + z + 3


@public
def get_property() -> int:
    obj = Example()
    return obj.some_property

from boa3.sc.compiletime import public


class Example:
    @property
    def some_property(self, arg: int) -> int:
        return arg


@public
def get_property() -> int:
    obj = Example()
    return obj.some_property(10)

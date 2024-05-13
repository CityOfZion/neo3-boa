from boa3.sc.compiletime import public


class Example:
    cvar = 10

    @property
    def some_property(self) -> int:
        return self.cvar


@public
def get_property() -> int:
    obj = Example()
    return obj.some_property

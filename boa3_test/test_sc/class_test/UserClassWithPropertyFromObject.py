from boa3.builtin import public


class Example:
    @property
    def some_property(self) -> int:
        return 1


@public
def get_property() -> int:
    obj = Example()
    return obj.some_property

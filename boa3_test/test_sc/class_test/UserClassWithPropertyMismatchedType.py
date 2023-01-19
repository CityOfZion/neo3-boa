from boa3.builtin.compile_time import public


class Example:
    @property
    def some_property(self) -> int:
        return 1


@public
def get_property() -> str:
    obj = Example()
    return obj.some_property

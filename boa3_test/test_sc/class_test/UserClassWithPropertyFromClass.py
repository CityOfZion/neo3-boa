from boa3.builtin.compile_time import public


class Example:
    @property
    def some_property(self) -> int:
        return 10


@public
def get_property() -> int:
    return Example.some_property

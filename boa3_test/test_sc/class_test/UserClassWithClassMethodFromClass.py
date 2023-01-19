from boa3.builtin.compile_time import public


class Example:
    @classmethod
    def some_method(cls) -> int:
        return 42


@public
def call_by_class_name() -> int:
    return Example.some_method()

from boa3.builtin.compile_time import public


class Example:
    def some_method(self) -> int:
        return 42


@public
def call_by_class_name() -> int:
    example = Example()
    return example.some_method()

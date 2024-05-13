from boa3.sc.compiletime import public


class Example:
    @classmethod
    def some_method(cls) -> int:
        return 42


@public
def call_by_class_name() -> int:
    example = Example()
    return example.some_method()

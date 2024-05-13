from boa3.sc.compiletime import public


class Example:
    def some_method(self) -> int:
        return 42


@public
def call_by_class_name() -> int:
    return Example().some_method()

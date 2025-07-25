from boa3.sc.compiletime import public


class Example:
    @staticmethod
    def some_method() -> int:
        return 42


def some_method() -> int:
    return 24


@public
def call_by_class_name() -> int:
    return Example.some_method()

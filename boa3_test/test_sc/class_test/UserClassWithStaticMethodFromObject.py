from boa3.builtin.compile_time import public


class Example:
    @staticmethod
    def some_method() -> int:
        return 42


@public
def call_by_class_name() -> int:
    return Example().some_method()

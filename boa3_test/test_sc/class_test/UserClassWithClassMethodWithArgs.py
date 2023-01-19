from boa3.builtin.compile_time import public


class Example:
    @classmethod
    def some_method(cls, arg0: int) -> int:
        return arg0


@public
def call_by_class_name(arg: int) -> int:
    return Example.some_method(arg)

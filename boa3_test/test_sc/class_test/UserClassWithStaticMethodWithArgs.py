from boa3.builtin.compile_time import public


class Example:
    @staticmethod
    def some_method(arg0: int, arg1: int) -> int:
        a = 10
        return a + arg0 + arg1


@public
def call_by_class_name(arg0: int, arg1: int) -> int:
    return Example.some_method(arg0, arg1)

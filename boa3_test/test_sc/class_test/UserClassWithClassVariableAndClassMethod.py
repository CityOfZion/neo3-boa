from boa3.builtin.compile_time import public


class Example:
    val1 = 1
    val2 = 42

    @classmethod
    def foo(cls) -> int:
        return cls.val2


@public
def get_val1() -> int:
    return Example.val1


@public
def get_foo() -> int:
    return Example.foo()

from boa3.builtin.compile_time import public


class Example:
    val1 = 1
    val2 = 2

    @classmethod
    def foo(cls) -> int:
        return cls.val1


@public
def get_val1() -> int:
    example = Example()
    return example.val1


@public
def get_val2() -> int:
    example = Example()
    return example.val2

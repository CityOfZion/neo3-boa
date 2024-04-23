from boa3.builtin.compile_time import public


@public
def Main(a: [int]) -> [int]:  # should be list[int] instead of [int]
    return a

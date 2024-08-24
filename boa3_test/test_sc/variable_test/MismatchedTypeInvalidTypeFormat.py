from boa3.sc.compiletime import public


@public
def Main(a: [int]) -> [int]:  # should be list[int] instead of [int]
    return a

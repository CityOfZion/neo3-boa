from boa3.builtin.compile_time import public


var1 = 42
var2 = '42'


@public
def Add(a: int, b: int) -> int:
    return a + b


@public
def Sub(a: int, b: int) -> int:
    return a - b

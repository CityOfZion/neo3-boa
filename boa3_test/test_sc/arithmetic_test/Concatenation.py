from boa3.builtin.compile_time import public


@public
def concat(a: str, b: str) -> str:
    return a + b

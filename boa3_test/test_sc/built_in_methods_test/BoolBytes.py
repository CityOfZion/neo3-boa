from boa3.builtin.compile_time import public


@public
def main(x: bytes) -> bool:
    return bool(x)

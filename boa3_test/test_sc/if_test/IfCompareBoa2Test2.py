from boa3.builtin.compile_time import public


@public
def main(a: int, b: int) -> bool:
    if a == b:
        return True
    return False

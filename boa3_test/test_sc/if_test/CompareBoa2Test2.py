from boa3.builtin import public


@public
def main(a: int, b: int) -> bool:
    if a == b:
        return True
    return False

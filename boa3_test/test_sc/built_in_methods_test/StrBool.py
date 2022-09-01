from boa3.builtin import public


@public
def main(value: bool) -> str:
    a = str(value)
    return a

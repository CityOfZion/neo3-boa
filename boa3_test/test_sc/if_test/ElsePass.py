from boa3.builtin import public


@public
def main(condition: bool) -> int:
    a = 0

    if condition:
        a = 5
    else:
        pass

    return a

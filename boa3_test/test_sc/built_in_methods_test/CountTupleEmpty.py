from boa3.builtin import public


@public
def main() -> int:
    a = ()
    return a.count(1)

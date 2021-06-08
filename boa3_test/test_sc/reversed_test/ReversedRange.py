from boa3.builtin import public


@public
def main() -> reversed:
    return reversed(range(3))

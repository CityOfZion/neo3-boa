from boa3.builtin import public


@public
def main(string: str) -> reversed:
    return reversed(string)

from boa3.builtin import public


@public
def main(string: str) -> bool:
    return string.isdigit()

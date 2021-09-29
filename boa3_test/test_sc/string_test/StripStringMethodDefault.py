from boa3.builtin import public


@public
def main(string: str) -> str:
    return string.strip()

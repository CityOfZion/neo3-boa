from boa3.builtin import public


@public
def main(value: str, some_string: str) -> bool:
    return value in some_string

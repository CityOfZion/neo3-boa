from boa3.sc.compiletime import public


@public
def main(value: str, some_string: str) -> bool:
    return value in some_string

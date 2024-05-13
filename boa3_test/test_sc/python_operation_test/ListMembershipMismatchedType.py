from boa3.sc.compiletime import public


@public
def main(value: int, some_list: list[str]) -> bool:
    return value not in some_list

from boa3.sc.compiletime import public


@public
def main(value: int, some_dict: dict[str, int]) -> bool:
    return value in some_dict

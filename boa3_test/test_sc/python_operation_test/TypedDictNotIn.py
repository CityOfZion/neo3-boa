from boa3.sc.compiletime import public


@public
def main(value: int, some_dict: dict[int, str]) -> bool:
    return value not in some_dict

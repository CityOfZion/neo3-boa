from boa3.builtin.compile_time import public


@public
def main(value: int, some_dict: dict[str, int]) -> bool:
    return value in some_dict

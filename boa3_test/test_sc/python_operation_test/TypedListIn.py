from boa3.builtin.compile_time import public


@public
def main(value: int, some_list: list[int]) -> bool:
    return value in some_list

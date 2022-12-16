from boa3.builtin.compile_time import public


@public
def main(value: str, some_string: str) -> bool:
    return value in some_string

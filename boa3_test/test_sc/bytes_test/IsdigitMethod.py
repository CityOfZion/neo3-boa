from boa3.builtin.compile_time import public


@public
def main(b_value: bytes) -> bool:
    return b_value.isdigit()

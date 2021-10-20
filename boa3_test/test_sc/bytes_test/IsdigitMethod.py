from boa3.builtin import public


@public
def main(b_value: bytes) -> bool:
    return b_value.isdigit()

from boa3.sc.compiletime import public


@public
def main(b_value: bytes) -> bool:
    return b_value.isdigit()

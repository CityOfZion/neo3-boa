from boa3.builtin import public


@public
def int_to_bytes() -> bytes:
    return (123).to_bytes()

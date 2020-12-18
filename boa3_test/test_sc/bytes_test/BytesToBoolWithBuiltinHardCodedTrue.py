from boa3.builtin import public


@public
def bytes_to_bool() -> bool:
    return bytes.to_bool(b'\x01')

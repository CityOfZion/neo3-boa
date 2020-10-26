from boa3.builtin import public


@public
def bytes_to_str() -> str:
    return bytes.to_str(b'123')

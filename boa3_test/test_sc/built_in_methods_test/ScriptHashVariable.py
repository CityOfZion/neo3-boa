from boa3.builtin import public


@public
def Main(a: bytes) -> bytes:
    return a.to_script_hash()

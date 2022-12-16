from boa3.builtin.compile_time import public


@public
def bytes_to_bool(args: bytes) -> bool:
    return bytes.to_bool(args)

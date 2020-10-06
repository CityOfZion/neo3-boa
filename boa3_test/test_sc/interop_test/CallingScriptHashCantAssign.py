from boa3.builtin.interop.runtime import calling_script_hash


def Main(example: bytes) -> bytes:
    global calling_script_hash
    calling_script_hash = example
    return calling_script_hash

from boa3.builtin.type.helper import to_bytes


def list_to_bytes() -> bytes:
    return to_bytes(['1', '2', '3'])

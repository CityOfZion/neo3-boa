from boa3.builtin.contract import to_script_hash


def Main() -> bytes:
    return to_script_hash(123, 123)

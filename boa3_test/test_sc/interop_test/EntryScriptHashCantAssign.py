from boa3.builtin.interop.runtime import entry_script_hash


def main(example: bytes) -> bytes:
    global entry_script_hash
    entry_script_hash = example
    return entry_script_hash

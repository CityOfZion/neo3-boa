from boa3.builtin.interop.blockchain import current_height


def Main(example: int) -> int:
    global current_height
    current_height = example
    return current_height

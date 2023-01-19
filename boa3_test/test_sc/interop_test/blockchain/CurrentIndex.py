from boa3.builtin.compile_time import public
from boa3.builtin.interop.blockchain import current_index


@public
def main() -> int:
    return current_index

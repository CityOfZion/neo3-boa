from boa3.builtin.compile_time import public
from boa3.builtin.interop.blockchain import Block


@public
def main() -> Block:
    return Block()

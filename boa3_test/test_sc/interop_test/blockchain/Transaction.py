from boa3.builtin.compile_time import public
from boa3.builtin.interop.blockchain import Transaction


@public
def main() -> Transaction:
    return Transaction()

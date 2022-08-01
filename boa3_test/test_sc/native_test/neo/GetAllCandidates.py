from boa3.builtin import public
from boa3.builtin.interop.iterator import Iterator
from boa3.builtin.nativecontract.neo import NEO


@public
def main() -> Iterator:
    return NEO.get_all_candidates()

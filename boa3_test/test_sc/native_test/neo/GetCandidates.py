from boa3.builtin.compile_time import public
from boa3.builtin.nativecontract.neo import NEO
from boa3.builtin.type import ECPoint


@public
def main() -> list[tuple[ECPoint, int]]:
    return NEO.get_candidates()

from typing import List

from boa3.builtin.compile_time import public
from boa3.builtin.nativecontract.neo import NEO
from boa3.builtin.type import ECPoint


@public
def main() -> List[ECPoint]:
    return NEO.get_next_block_validators()

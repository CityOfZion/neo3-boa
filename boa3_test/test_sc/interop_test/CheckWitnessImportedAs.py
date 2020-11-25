from boa3.builtin import public
from boa3.builtin.interop.runtime import check_witness as CheckWitness


@public
def Main(script_hash: bytes) -> bool:
    return CheckWitness(script_hash)

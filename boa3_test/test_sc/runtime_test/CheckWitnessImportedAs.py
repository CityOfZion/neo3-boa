from boa3.sc.compiletime import public
from boa3.sc.runtime import check_witness as CheckWitness
from boa3.sc.types import ECPoint


@public
def Main(script_hash: ECPoint) -> bool:
    return CheckWitness(script_hash)

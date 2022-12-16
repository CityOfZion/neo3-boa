from boa3.builtin.compile_time import public
from boa3.builtin.interop.runtime import check_witness
from boa3.builtin.type import ECPoint


@public
def Main(script_hash: ECPoint) -> bool:
    return check_witness(script_hash)

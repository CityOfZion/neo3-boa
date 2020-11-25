from boa3.builtin import public
from boa3.builtin.interop.runtime import check_witness


@public
def Main(script_hash: bytes) -> bool:
    return check_witness(script_hash)

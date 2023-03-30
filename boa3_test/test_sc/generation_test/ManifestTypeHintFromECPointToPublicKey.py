from boa3.builtin.compile_time import public
from boa3.builtin.type import ECPoint, PublicKey


@public
def Main() -> PublicKey:
    return ECPoint(b'')

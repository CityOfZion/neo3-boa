from boa3.builtin.compile_time import public
from boa3.builtin.interop.contract import create_standard_account
from boa3.builtin.type import ECPoint, UInt160


@public
def main(public_key: bytes) -> UInt160:
    return create_standard_account(ECPoint(public_key))

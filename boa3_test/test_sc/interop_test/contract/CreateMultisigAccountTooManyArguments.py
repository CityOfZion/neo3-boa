from typing import Any, List

from boa3.builtin.interop.contract import create_multisig_account
from boa3.builtin.type import ECPoint, UInt160


def main(minimum_sigs: int, public_keys: List[ECPoint], arg: Any) -> UInt160:
    return create_multisig_account(minimum_sigs, public_keys, arg)

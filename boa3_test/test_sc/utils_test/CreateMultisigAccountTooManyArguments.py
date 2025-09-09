from typing import Any

from boa3.sc.types import ECPoint, UInt160
from boa3.sc.utils import create_multisig_account


def main(minimum_sigs: int, public_keys: list[ECPoint], arg: Any) -> UInt160:
    return create_multisig_account(minimum_sigs, public_keys, arg)

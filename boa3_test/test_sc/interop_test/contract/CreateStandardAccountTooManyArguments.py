from typing import Any

from boa3.builtin.interop.contract import create_standard_account
from boa3.builtin.type import ECPoint, UInt160


def main(public_key: bytes, arg1: Any) -> UInt160:
    return create_standard_account(ECPoint(public_key), arg1)

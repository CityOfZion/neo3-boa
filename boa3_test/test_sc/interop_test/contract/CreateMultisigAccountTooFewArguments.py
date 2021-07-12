from boa3.builtin.interop.contract import create_multisig_account
from boa3.builtin.type import UInt160


def main(minimum_sigs: int) -> UInt160:
    return create_multisig_account(minimum_sigs)

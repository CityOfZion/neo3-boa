from boa3.sc.utils import create_multisig_account
from boa3.sc.types import UInt160


def main(minimum_sigs: int) -> UInt160:
    return create_multisig_account(minimum_sigs)

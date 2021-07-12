from boa3.builtin.interop.contract import create_standard_account
from boa3.builtin.type import UInt160


def main() -> UInt160:
    return create_standard_account()

from boa3.builtin import public
from boa3.builtin.interop.runtime import address_version


@public
def main() -> int:
    address_version = 123
    return address_version


def interop_call():
    x = address_version

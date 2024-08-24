from boa3.sc.compiletime import public
from boa3.sc.runtime import address_version


@public
def main() -> int:
    address_version = 123
    return address_version


def interop_call():
    x = address_version

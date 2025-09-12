from boa3.sc.compiletime import public
from boa3.sc.runtime import address_version


@public
def main() -> int:
    return address_version

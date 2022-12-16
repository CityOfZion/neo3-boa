from boa3.builtin.compile_time import public
from boa3.builtin.interop.runtime import address_version


@public
def main() -> int:
    return address_version

from boa3.builtin import public
from boa3.builtin.interop.storage.findoptions import FindOptions


@public
def main(a: FindOptions) -> int:
    return ~a
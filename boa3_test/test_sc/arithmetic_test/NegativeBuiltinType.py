from boa3.builtin.compile_time import public
from boa3.builtin.interop.storage.findoptions import FindOptions


@public
def minus(a: FindOptions) -> int:
    return -a

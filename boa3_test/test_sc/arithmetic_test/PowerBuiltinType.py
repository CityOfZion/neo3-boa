from boa3.builtin.compile_time import public
from boa3.builtin.interop.storage.findoptions import FindOptions


@public
def main(option1: FindOptions, option2: FindOptions) -> int:
    return option1 ** option2

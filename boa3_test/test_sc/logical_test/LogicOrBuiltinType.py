from boa3.builtin.compile_time import public
from boa3.sc.types import FindOptions


@public
def main(option1: FindOptions, option2: FindOptions) -> int:
    flags = option1 | option2
    return option1 | option2 

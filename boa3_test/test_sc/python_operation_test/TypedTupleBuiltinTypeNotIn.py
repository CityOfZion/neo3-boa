from boa3.builtin.compile_time import public
from boa3.sc.types.findoptions import FindOptions


@public
def main(value: FindOptions, some_tuple: tuple[FindOptions]) -> bool:
    return value not in some_tuple

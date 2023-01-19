from typing import Tuple

from boa3.builtin.compile_time import public
from boa3.builtin.interop.storage.findoptions import FindOptions


@public
def main(value: FindOptions, some_tuple: Tuple[FindOptions]) -> bool:
    return value in some_tuple

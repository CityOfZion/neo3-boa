from typing import List

from boa3.builtin import public
from boa3.builtin.interop.storage.findoptions import FindOptions


@public
def main(value: FindOptions, some_list: List[FindOptions]) -> bool:
    return value in some_list

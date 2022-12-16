from typing import Dict

from boa3.builtin.compile_time import public
from boa3.builtin.interop.storage.findoptions import FindOptions


@public
def main(value: FindOptions, some_dict: Dict[FindOptions, str]) -> bool:
    return value not in some_dict

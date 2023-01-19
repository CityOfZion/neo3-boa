from typing import List

# only compile if pass boa3_test/test_sc/generation_test as project root
from GenerationWithUserModuleImports import with_param

from boa3.builtin.compile_time import public
from boa3.builtin.interop.runtime import Notification
from boa3.builtin.type import UInt160


@public
def main(args: list, key: UInt160) -> List[Notification]:
    return with_param(args, key)

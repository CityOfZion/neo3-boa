from typing import List

# only compile if pass boa3_test as project root
from test_sc.interop_test.runtime.GetNotifications import with_param

from boa3.builtin import public
from boa3.builtin.interop.runtime import Notification
from boa3.builtin.type import UInt160


@public
def main(args: list, key: UInt160) -> List[Notification]:
    return with_param(args, key)

from typing import List

from boa3.builtin import public
from boa3.builtin.interop.runtime import Notification
from boa3.builtin.type import UInt160
from boa3_test.test_sc.interop_test.runtime.GetNotifications import with_param


@public
def main(args: list, key: UInt160) -> List[Notification]:
    return with_param(args, key)

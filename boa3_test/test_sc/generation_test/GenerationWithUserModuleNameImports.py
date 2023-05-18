from typing import List

from boa3.builtin.compile_time import public
from boa3.builtin.interop.runtime import Notification
from boa3.builtin.type import UInt160
from boa3_test.test_sc.interop_test.runtime import GetNotifications


@public
def main(args: list, key: UInt160) -> List[Notification]:
    return GetNotifications.with_param(args, key)

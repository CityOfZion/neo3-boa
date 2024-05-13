from boa3.sc.compiletime import public
from boa3.sc.types import UInt160, Notification
from boa3_test.test_sc.interop_test.runtime.GetNotifications import with_param


@public
def main(args: list, key: UInt160) -> list[Notification]:
    return with_param(args, key)

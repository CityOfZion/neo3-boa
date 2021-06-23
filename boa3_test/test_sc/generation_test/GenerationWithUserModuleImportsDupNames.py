from typing import List

import boa3_test.test_sc.dict_test.GetValue as DictGet
import boa3_test.test_sc.list_test.GetValue as ListGet
import boa3_test.test_sc.range_test.GetValue as RangeGet
import boa3_test.test_sc.string_test.GetValue as StringGet
import boa3_test.test_sc.tuple_test.GetValue as TupleGet
from boa3.builtin import public
from boa3.builtin.interop.runtime import Notification
from boa3.builtin.type import UInt160
from boa3_test.test_sc.interop_test.runtime.GetNotifications import with_param


@public
def main(args: list, key: UInt160) -> List[Notification]:
    return with_param(args, key)

from typing import Any, List

from boa3.builtin.compile_time import public
from boa3_test.test_sc.import_test.FromImportTyping import EmptyList as NewList


@public
def Main() -> list:
    a: List[Any] = NewList()
    return a

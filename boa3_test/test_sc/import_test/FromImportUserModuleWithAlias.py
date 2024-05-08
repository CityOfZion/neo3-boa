from typing import Any

from boa3.builtin.compile_time import public
from boa3_test.test_sc.import_test.FromImportTyping import EmptyList as NewList


@public
def Main() -> list:
    a: list[Any] = NewList()
    return a

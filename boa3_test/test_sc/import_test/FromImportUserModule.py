from typing import Any

from boa3.sc.compiletime import public
from boa3_test.test_sc.import_test.FromImportTyping import EmptyList


@public
def Main() -> list:
    a: list[Any] = EmptyList()
    return a

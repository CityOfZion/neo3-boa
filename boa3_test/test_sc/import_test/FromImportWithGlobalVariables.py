from typing import Any

from boa3.sc.compiletime import public
from boa3_test.test_sc.import_test.FromImportTyping import EmptyList

a = EmptyList()


@public
def Main() -> list[Any]:
    return a

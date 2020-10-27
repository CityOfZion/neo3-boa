from typing import Any, List

from boa3.builtin import public
from boa3_test.test_sc.import_test.FromImportTyping import EmptyList

a = EmptyList()


@public
def Main() -> List[Any]:
    return a

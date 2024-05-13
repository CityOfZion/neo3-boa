from typing import Any

import boa3_test.test_sc.import_test.FromImportTyping
from boa3.sc.compiletime import public


@public
def Main() -> list[Any]:
    return boa3_test.test_sc.import_test.FromImportTyping.EmptyList()

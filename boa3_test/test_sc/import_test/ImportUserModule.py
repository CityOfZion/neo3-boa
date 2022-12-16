from typing import Any, List

import boa3_test.test_sc.import_test.FromImportTyping
from boa3.builtin.compile_time import public


@public
def Main() -> List[Any]:
    return boa3_test.test_sc.import_test.FromImportTyping.EmptyList()

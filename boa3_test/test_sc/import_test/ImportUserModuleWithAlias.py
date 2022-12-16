from typing import Any, List

import boa3_test.test_sc.import_test.FromImportTyping as UserModule
from boa3.builtin.compile_time import public


@public
def Main() -> List[Any]:
    return UserModule.EmptyList()

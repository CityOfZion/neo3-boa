from typing import Any

import boa3_test.test_sc.import_test.FromImportTyping as UserModule
from boa3.builtin.compile_time import public


@public
def Main() -> list[Any]:
    return UserModule.EmptyList()

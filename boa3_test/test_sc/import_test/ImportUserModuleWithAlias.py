from typing import Any

import boa3_test.test_sc.import_test.FromImportTyping as UserModule
from boa3.sc.compiletime import public


@public
def Main() -> list[Any]:
    return UserModule.EmptyList()

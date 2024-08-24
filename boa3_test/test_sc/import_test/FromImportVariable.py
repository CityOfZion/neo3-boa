from typing import Any

from boa3.sc.compiletime import public
from boa3_test.test_sc.import_test.FromImportTyping import empty_list


@public
def Main() -> list[Any]:
    return empty_list

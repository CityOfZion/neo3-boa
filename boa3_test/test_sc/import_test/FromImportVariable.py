from typing import Any, List

from boa3.builtin.compile_time import public
from boa3_test.test_sc.import_test.FromImportTyping import empty_list


@public
def Main() -> List[Any]:
    return empty_list

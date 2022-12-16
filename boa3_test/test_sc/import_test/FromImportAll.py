from boa3.builtin.compile_time import public

from boa3_test.test_sc.import_test.FromImportTyping import *


@public
def call_imported_method() -> list:
    a: List[Any] = EmptyList()
    return a


@public
def call_imported_variable() -> list:
    return empty_list

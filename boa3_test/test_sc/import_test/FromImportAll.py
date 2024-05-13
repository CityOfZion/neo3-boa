from boa3.sc.compiletime import public

from boa3_test.test_sc.import_test.FromImportTyping import *


@public
def call_imported_method() -> list:
    a: list[Any] = EmptyList()
    return a


@public
def call_imported_variable() -> list:
    return empty_list

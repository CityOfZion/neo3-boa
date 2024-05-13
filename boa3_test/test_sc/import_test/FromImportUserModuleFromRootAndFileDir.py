from typing import Any

from boa3.sc.compiletime import public
from boa3_test.test_sc.import_test.FromImportTyping import EmptyList as RootImportedFunction
from package_with_import.Module import EmptyList as FileDirImportedFunction


@public
def call_imported_from_root() -> list:
    a: list[Any] = RootImportedFunction()
    return a


@public
def call_imported_from_file_dir() -> list:
    a: list[Any] = FileDirImportedFunction()
    return a

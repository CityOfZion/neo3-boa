from boa3.builtin.compile_time import public
from boa3_test.test_sc.import_test.FromImportUserModuleRecursiveImport import from_import_empty_list


@public
def empty_list() -> list:
    return from_import_empty_list()

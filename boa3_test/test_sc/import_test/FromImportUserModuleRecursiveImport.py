from boa3.builtin.compile_time import public
from boa3_test.test_sc.import_test.ImportUserModuleRecursiveImport import import_empty_list


@public
def from_import_empty_list() -> list:
    return import_empty_list()

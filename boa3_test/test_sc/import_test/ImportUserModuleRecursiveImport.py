import boa3_test.test_sc.import_test.UserModuleWithRecursiveImport
from boa3.builtin.compile_time import public


@public
def import_empty_list() -> list:
    return boa3_test.test_sc.import_test.UserModuleWithRecursiveImport.empty_list()

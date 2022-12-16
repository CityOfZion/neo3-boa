from boa3.builtin.compile_time import public

from boa3_test.test_sc.import_test.package_with_import import Module


@public
def call_imported_method() -> list:
    a: Module.List[Module.Any] = Module.EmptyList()
    return a


@public
def call_imported_variable() -> int:
    return Module.default_number

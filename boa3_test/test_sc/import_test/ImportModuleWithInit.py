from boa3.sc.compiletime import public

from boa3_test.test_sc.import_test.package_with_import import Module


@public
def call_imported_method() -> list:
    a: list[Module.Any] = Module.EmptyList()
    return a


@public
def call_imported_variable() -> int:
    return Module.default_number

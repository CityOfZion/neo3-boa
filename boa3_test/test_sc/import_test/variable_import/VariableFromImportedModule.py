import boa3_test.test_sc.import_test.variable_import.GenerateImportedVariable as OtherModule
from boa3.builtin.compile_time import public


@public
def get_foo() -> bytes:
    return OtherModule.foo()


@public
def get_bar() -> str:
    return OtherModule.bar()

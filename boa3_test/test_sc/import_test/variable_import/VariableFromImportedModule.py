import boa3_test.test_sc.import_test.variable_import.GenerateImportedVariable as OtherModule
# TODO: remove when the bug that doesn't initialize global variables from modules that are not imported in the main
#  file is fixed
import boa3_test.test_sc.import_test.variable_import.StaticVariables as StaticVariables
from boa3.builtin import public


@public
def get_foo() -> bytes:
    return OtherModule.foo()


@public
def get_bar() -> str:
    return OtherModule.bar()

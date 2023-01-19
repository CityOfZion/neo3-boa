
import boa3_test.test_sc.import_test.variable_import.StaticVariables as StaticVariables
from boa3.builtin.compile_time import public


@public
def get_foo() -> bytes:
    return StaticVariables.FOO


@public
def get_bar() -> str:
    return StaticVariables.BAR

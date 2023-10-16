from typing import Any

from boa3.builtin.compile_time import public
from boa3_test.test_sc.variable_test.ListGlobalAssignment import get_from_global

a = 42  # same name of a variable in a imported package


@public
def value_from_import() -> Any:
    return get_from_global()


@public
def value_from_script() -> Any:
    return a

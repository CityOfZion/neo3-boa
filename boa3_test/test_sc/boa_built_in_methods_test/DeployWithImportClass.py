from typing import Any

from boa3.sc.compiletime import public
from boa3.sc.storage import get, put
from boa3.sc.contracts.stdlib import StdLib

from boa3_test.test_sc.import_test.class_import.example import Example
from boa3_test.test_sc.import_test.class_import.ImportUserClass import build_example_object

key = b'1'


@public
def main() -> Example:
    example: Example = StdLib.deserialize(get(key))
    return example


@public
def _deploy(data: Any, update: bool):
    put(key, StdLib.serialize(build_example_object()))
    return None

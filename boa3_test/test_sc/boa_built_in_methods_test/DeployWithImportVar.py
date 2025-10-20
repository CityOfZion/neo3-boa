from typing import Any

from boa3.sc.compiletime import public
from boa3.sc.storage import put_str, get_str

from boa3_test.test_sc.import_test.variable_import.StaticVariables import BAR

key = b'1'


@public
def main() -> str:
    return get_str(key)


@public
def _deploy(data: Any, update: bool):
    put_str(key, BAR)
    return None

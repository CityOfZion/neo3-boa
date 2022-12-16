from typing import Any, Dict

from boa3.builtin.compile_time import public
from package_with_import import Module as imported_module


@public
def get_token_json(token_id: bytes) -> Dict[str, Any]:
    return imported_module.get_token_json(token_id)  # this method doesn't exist in the imported module

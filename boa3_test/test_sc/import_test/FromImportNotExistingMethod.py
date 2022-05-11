from typing import Any, Dict

from package_with_import import Module as imported_module

from boa3.builtin import public


@public
def get_token_json(token_id: bytes) -> Dict[str, Any]:
    return imported_module.get_token_json(token_id)  # this method doesn't exist in the imported module

from typing import Any

from boa3.sc.compiletime import public
from package_with_import import Module as imported_module


@public
def get_token_json(token_id: bytes) -> dict[str, Any]:
    return imported_module.get_token_json(token_id)  # this method doesn't exist in the imported module

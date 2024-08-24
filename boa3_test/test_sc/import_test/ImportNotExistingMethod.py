from typing import Any

import FromImportAll as imported_module
from boa3.sc.compiletime import public


@public
def get_token_json(token_id: bytes) -> dict[str, Any]:
    return imported_module.get_token_json(token_id)  # this method doesn't exist in the imported module

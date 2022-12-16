from typing import Any, Dict

import FromImportAll as imported_module
from boa3.builtin.compile_time import public


@public
def get_token_json(token_id: bytes) -> Dict[str, Any]:
    return imported_module.get_token_json(token_id)  # this method doesn't exist in the imported module

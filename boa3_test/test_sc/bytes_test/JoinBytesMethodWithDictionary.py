from typing import Any, Dict

from boa3.builtin import public


@public
def main(string: bytes, dictionary: Dict[bytes, Any]) -> bytes:
    return string.join(dictionary)

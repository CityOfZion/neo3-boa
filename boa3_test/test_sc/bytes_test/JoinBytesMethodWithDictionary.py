from typing import Any

from boa3.sc.compiletime import public


@public
def main(string: bytes, dictionary: dict[bytes, Any]) -> bytes:
    return string.join(dictionary)

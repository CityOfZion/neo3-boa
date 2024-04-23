from typing import Any

from boa3.builtin.compile_time import public


@public
def main(string: bytes, dictionary: dict[bytes, Any]) -> bytes:
    return string.join(dictionary)

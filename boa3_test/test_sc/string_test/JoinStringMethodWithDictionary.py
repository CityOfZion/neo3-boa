from typing import Any

from boa3.builtin.compile_time import public


@public
def main(string: str, dictionary: dict[str, Any]) -> str:
    return string.join(dictionary)

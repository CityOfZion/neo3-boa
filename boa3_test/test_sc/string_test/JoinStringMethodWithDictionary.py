from typing import Any, Dict

from boa3.builtin.compile_time import public


@public
def main(string: str, dictionary: Dict[str, Any]) -> str:
    return string.join(dictionary)

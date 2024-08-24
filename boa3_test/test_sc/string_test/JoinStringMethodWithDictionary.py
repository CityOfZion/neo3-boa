from typing import Any

from boa3.sc.compiletime import public


@public
def main(string: str, dictionary: dict[str, Any]) -> str:
    return string.join(dictionary)

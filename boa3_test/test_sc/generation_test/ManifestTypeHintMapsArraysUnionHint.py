from typing import Union

from boa3.builtin.compile_time import public


@public
def Main(var: dict[str, list[bool]]) -> list[Union[dict[str, int], str, bool]]:
    if var:
        return []
    return []

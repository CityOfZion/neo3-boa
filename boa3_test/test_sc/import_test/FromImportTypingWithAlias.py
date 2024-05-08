from typing import Any as Bar

from boa3.builtin.compile_time import public


@public
def EmptyList() -> list[Bar]:
    return []

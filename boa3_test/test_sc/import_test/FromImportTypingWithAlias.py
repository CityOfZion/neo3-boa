from typing import Any as Bar, List as Foo

from boa3.builtin.compile_time import public


@public
def EmptyList() -> Foo[Bar]:
    return []

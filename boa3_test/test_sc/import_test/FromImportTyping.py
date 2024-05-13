from typing import Any

from boa3.sc.compiletime import \
    public as public_method  # alias to not change other tests when executing lint process


@public_method
def EmptyList() -> list[Any]:
    return []


empty_list = []

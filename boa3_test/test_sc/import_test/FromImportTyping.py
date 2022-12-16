from typing import Any, List

from boa3.builtin.compile_time import \
    public as public_method  # alias to not change other tests when executing lint process


@public_method
def EmptyList() -> List[Any]:
    return []


empty_list = []

from typing import Optional

from boa3.builtin.compile_time import public


@public
def main(var: Optional[int, str]) -> Optional[int]:
    if isinstance(var, int):
        return 123
    else:
        return None

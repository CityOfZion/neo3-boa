from typing import Optional

from boa3.builtin.compile_time import public


@public
def main(param: Optional[str]) -> Optional[str]:
    other = param or "some default value"
    return other

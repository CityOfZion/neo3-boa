from typing import Optional

from boa3.builtin.compile_time import public
from boa3.builtin.contract import abort


@public
def main(check: bool, message: Optional[str]) -> int:
    if check:
        abort(message)
    return 123

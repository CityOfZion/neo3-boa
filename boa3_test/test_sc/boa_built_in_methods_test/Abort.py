from boa3.builtin import public
from boa3.builtin.contract import abort


@public
def main(check: bool) -> int:
    if check:
        abort()
    return 123

from boa3.builtin.compile_time import public
from boa3.builtin.contract import abort


@public
def main(check: bool) -> int:
    if check:
        abort('abort was called')
    return 123

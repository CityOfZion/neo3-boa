from boa3.sc.compiletime import public
from boa3.sc.utils import abort


@public
def main(check: bool) -> int:
    if check:
        abort('abort was called')
    return 123

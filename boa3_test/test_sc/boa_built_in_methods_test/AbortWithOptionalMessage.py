from boa3.sc.compiletime import public
from boa3.sc.utils import abort


@public
def main(check: bool, message: str | None) -> int:
    if check:
        abort(message)
    return 123

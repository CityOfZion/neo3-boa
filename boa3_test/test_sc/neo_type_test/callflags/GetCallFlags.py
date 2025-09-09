from boa3.sc.compiletime import public
from boa3.sc.types import CallFlags
from boa3.sc.utils import get_call_flags


@public
def main() -> CallFlags:
    return get_call_flags()

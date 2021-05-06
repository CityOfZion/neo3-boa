from boa3.builtin import public
from boa3.builtin.interop.contract import CallFlags, get_call_flags


@public
def main() -> CallFlags:
    return get_call_flags()

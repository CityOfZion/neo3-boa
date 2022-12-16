from boa3.builtin.compile_time import public
from boa3.builtin.interop.contract import CallFlags, get_call_flags


@public
def main() -> CallFlags:
    return get_call_flags()

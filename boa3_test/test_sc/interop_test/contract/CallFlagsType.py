from boa3.builtin.compile_time import public
from boa3.builtin.interop.contract import CallFlags


@public
def main(flag: str) -> CallFlags:
    call_flags: CallFlags
    if flag == 'ALL':
        call_flags = CallFlags.ALL
    elif flag == 'READ_ONLY':
        call_flags = CallFlags.READ_ONLY
    elif flag == 'STATES':
        call_flags = CallFlags.STATES
    elif flag == 'ALLOW_NOTIFY':
        call_flags = CallFlags.ALLOW_NOTIFY
    elif flag == 'ALLOW_CALL':
        call_flags = CallFlags.ALLOW_CALL
    elif flag == 'WRITE_STATES':
        call_flags = CallFlags.WRITE_STATES
    elif flag == 'READ_STATES':
        call_flags = CallFlags.READ_STATES
    else:
        call_flags = CallFlags.NONE

    return call_flags

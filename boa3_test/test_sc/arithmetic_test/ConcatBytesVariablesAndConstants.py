from boa3.builtin import public
from boa3.builtin.interop.runtime import get_time


VALUE1 = b'value1'
VALUE2 = b'value2'
VALUE3 = b'value3'


@public
def concat() -> bytes:
    current_time = get_time.to_bytes()
    return VALUE1 + b'  ' + VALUE2 + b'  ' + VALUE3 + b'  ' + current_time

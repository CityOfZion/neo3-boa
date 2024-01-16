from boa3.builtin.compile_time import public
from boa3.builtin.interop import runtime


@public
def hello_world() -> str:
    runtime.notify('Hello World!')
    return 'Test'

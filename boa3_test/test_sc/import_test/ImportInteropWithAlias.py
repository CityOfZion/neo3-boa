from boa3.builtin import interop as functions
from boa3.builtin.compile_time import public


@public
def Main():
    functions.runtime.notify('something')

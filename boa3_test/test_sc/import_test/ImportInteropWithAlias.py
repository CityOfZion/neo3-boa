from boa3.builtin import interop as functions
from boa3.sc.compiletime import public


@public
def Main():
    functions.runtime.notify('something')

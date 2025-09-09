from boa3 import sc as functions
from boa3.sc.compiletime import public


@public
def Main():
    functions.runtime.notify('something')

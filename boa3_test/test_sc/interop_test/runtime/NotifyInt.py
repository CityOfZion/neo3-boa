from boa3.builtin.compile_time import public
from boa3.builtin.interop.runtime import notify


@public
def Main():
    notify(15)

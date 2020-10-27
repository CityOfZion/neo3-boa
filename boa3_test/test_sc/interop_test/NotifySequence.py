from boa3.builtin import public

from boa3.builtin.interop.runtime import notify


@public
def Main():
    notify([2, 3, 5, 7])

from boa3.sc.compiletime import public

from boa3.sc.runtime import notify


@public
def Main():
    notify(10, 'unit_test')

from boa3.sc.compiletime import public
from boa3.sc.runtime import notify


@public
def Main():
    notify([2, 3, 5, 7])

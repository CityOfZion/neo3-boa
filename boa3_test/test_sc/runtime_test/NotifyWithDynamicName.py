from boa3.sc.compiletime import public

from boa3.sc.runtime import notify


@public
def Main(notify_name: str):
    notify(10, notify_name)

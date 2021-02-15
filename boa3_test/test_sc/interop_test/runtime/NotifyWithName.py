from boa3.builtin import public

from boa3.builtin.interop.runtime import notify


@public
def Main(notify_name: str):
    notify(10, notify_name)

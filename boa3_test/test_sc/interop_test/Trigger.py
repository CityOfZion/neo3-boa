from boa3.builtin import public

from boa3.builtin.interop.runtime import TriggerType, trigger


@public
def Main() -> TriggerType:
    return trigger()

from boa3.builtin import public

from boa3.builtin.interop.runtime import TriggerType, trigger


@public
def Main() -> bool:
    return trigger() == TriggerType.APPLICATION

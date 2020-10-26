from boa3.builtin import public

from boa3.builtin.interop.runtime import TriggerType as Trigger, trigger


@public
def Main() -> bool:
    return trigger() == Trigger.VERIFICATION

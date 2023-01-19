from boa3.builtin.compile_time import public
from boa3.builtin.interop.runtime import TriggerType as Trigger, get_trigger


@public
def Main() -> bool:
    return get_trigger() == Trigger.VERIFICATION

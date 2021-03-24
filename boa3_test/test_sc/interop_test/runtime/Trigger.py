from boa3.builtin import public
from boa3.builtin.interop.runtime import TriggerType, get_trigger


@public
def Main() -> TriggerType:
    return get_trigger()

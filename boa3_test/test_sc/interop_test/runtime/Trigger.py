from boa3.builtin.compile_time import public
from boa3.builtin.interop.runtime import TriggerType, get_trigger


@public
def Main() -> TriggerType:
    return get_trigger()

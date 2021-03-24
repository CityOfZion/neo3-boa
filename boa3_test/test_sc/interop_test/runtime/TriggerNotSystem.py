from boa3.builtin.interop.runtime import TriggerType, get_trigger


def Main() -> bool:
    return get_trigger() != TriggerType.SYSTEM

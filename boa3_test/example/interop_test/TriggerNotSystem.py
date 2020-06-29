from boa3.builtin.interop.runtime import trigger, TriggerType


def Main() -> bool:
    return trigger() != TriggerType.SYSTEM

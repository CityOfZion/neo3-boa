from boa3.builtin.interop.runtime import TriggerType, trigger


def Main() -> bool:
    return trigger() == TriggerType.APPLICATION

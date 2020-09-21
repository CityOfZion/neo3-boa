from boa3.builtin.interop.runtime import TriggerType as Trigger, trigger


def Main() -> bool:
    return trigger() == Trigger.VERIFICATION

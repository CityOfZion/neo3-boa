from boa3.builtin.interop.runtime import trigger, TriggerType as Trigger


def Main() -> bool:
    return trigger() == Trigger.VERIFICATION

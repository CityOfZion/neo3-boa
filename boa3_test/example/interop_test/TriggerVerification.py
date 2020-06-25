from boa3.interop.runtime import trigger, TriggerType as Trigger


def Main() -> bool:
    return trigger() == Trigger.VERIFICATION

from enum import IntFlag


class TriggerType(IntFlag):
    SYSTEM = 0x01
    VERIFICATION = 0x20
    APPLICATION = 0x40
    ALL = SYSTEM | VERIFICATION | APPLICATION

from boa3.builtin.compile_time import CreateNewEvent
from boa3.builtin.type import PublicKey


Event = CreateNewEvent(
    [
        ('a', PublicKey)
    ]
)


def Main():
    Event('10')

from boa3.builtin.compile_time import CreateNewEvent
from boa3.builtin.type import UInt256

Event = CreateNewEvent(
    [
        ('a', UInt256)
    ]
)


def Main():
    Event('10')

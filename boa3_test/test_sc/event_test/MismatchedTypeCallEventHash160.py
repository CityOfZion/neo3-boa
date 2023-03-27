from boa3.builtin.compile_time import CreateNewEvent
from boa3.builtin.type import UInt160

Event = CreateNewEvent(
    [
        ('a', UInt160)
    ]
)


def Main():
    Event('10')

from boa3.sc.types import UInt160
from boa3.sc.utils import CreateNewEvent

Event = CreateNewEvent(
    [
        ('a', UInt160)
    ]
)


def Main():
    Event('10')

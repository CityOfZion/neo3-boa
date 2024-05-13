from boa3.sc.types import UInt256
from boa3.sc.utils import CreateNewEvent

Event = CreateNewEvent(
    [
        ('a', UInt256)
    ]
)


def Main():
    Event('10')

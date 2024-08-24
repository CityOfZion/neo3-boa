from boa3.sc.types import PublicKey
from boa3.sc.utils import CreateNewEvent

Event = CreateNewEvent(
    [
        ('a', PublicKey)
    ]
)


def Main():
    Event('10')

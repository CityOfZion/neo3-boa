from boa3.sc.utils import CreateNewEvent
from boa3.sc.utils.iterator import Iterator

Event = CreateNewEvent(
    [
        ('a', Iterator)  # this shouldn't compile
    ]
)


def Main() -> bool:
    return False

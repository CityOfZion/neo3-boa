from boa3.sc.compiletime import public
from boa3.sc.utils import CreateNewEvent

Event = CreateNewEvent(
    [
        ('a', int)
    ]
)


@public
def Main():
    Event(10)

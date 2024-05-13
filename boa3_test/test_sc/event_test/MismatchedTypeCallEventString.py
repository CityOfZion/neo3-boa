from boa3.sc.utils import CreateNewEvent

Event = CreateNewEvent(
    [
        ('a', str)
    ]
)


def Main():
    Event(b'10')

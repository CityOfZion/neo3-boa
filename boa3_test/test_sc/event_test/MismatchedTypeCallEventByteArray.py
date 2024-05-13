from boa3.sc.utils import CreateNewEvent

Event = CreateNewEvent(
    [
        ('a', bytes)
    ]
)


def Main():
    Event('10')

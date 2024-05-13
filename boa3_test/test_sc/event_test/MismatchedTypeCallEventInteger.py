from boa3.sc.utils import CreateNewEvent

Event = CreateNewEvent(
    [
        ('a', int)
    ]
)


def Main():
    Event('10')

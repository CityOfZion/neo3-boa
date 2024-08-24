from boa3.sc.utils import CreateNewEvent

Event = CreateNewEvent(
    [
        ('a', dict)
    ]
)


def Main():
    Event('10')

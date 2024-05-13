from boa3.sc.utils import CreateNewEvent

Event = CreateNewEvent(
    [
        ('a', list)
    ]
)


def Main():
    Event('10')

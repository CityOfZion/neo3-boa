from boa3.sc.utils import CreateNewEvent

Event = CreateNewEvent(
    [
        ('a', bool)
    ]
)


def Main():
    Event('10')

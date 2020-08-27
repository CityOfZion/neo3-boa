from boa3.builtin import CreateNewEvent


Event = CreateNewEvent(
    [
        ('a', int)
    ]
)


def Main():
    Event(10)

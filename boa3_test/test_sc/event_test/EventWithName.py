from boa3.builtin import CreateNewEvent


Event = CreateNewEvent(
    [
        ('a', int)
    ],
    'example'
)


def Main():
    Event(10)

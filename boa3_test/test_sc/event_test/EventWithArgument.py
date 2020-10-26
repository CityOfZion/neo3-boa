from boa3.builtin import CreateNewEvent, public

Event = CreateNewEvent(
    [
        ('a', int)
    ]
)


@public
def Main():
    Event(10)

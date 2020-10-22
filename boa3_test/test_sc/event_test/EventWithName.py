from boa3.builtin import CreateNewEvent, public

Event = CreateNewEvent(
    [
        ('a', int)
    ],
    'example'
)


@public
def Main():
    Event(10)

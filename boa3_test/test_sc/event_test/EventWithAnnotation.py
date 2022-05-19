from boa3.builtin import CreateNewEvent, Event, public

on_example: Event = CreateNewEvent(
    [
        ('a', int)
    ],
    'example'
)


@public
def Main():
    on_example(10)

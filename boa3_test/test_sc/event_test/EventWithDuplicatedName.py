from boa3.builtin import CreateNewEvent, public

on_event = CreateNewEvent(
    [
        ('a', int)
    ],
    'example'
)


@public
def example(arg: int):
    on_event(arg)

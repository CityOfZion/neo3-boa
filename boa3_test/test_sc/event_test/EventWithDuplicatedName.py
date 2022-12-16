from boa3.builtin.compile_time import public, CreateNewEvent

on_event = CreateNewEvent(
    [
        ('a', int)
    ],
    'example'
)


@public
def example(arg: int):
    on_event(arg)

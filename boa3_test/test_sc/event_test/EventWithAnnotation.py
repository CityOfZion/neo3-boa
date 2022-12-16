from boa3.builtin.compile_time import public, CreateNewEvent
from boa3.builtin.type import Event

on_example: Event = CreateNewEvent(
    [
        ('a', int)
    ],
    'example'
)


@public
def Main():
    on_example(10)

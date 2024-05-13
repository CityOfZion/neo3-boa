from boa3.sc.compiletime import public
from boa3.sc.types import Event
from boa3.sc.utils import CreateNewEvent

on_example: Event = CreateNewEvent(
    [
        ('a', int)
    ],
    'example'
)


@public
def Main():
    on_example(10)

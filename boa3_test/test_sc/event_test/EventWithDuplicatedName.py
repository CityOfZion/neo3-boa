from boa3.sc.compiletime import public
from boa3.sc.utils import CreateNewEvent

on_event = CreateNewEvent(
    [
        ('a', int)
    ],
    'example'
)


@public
def example(arg: int):
    on_event(arg)

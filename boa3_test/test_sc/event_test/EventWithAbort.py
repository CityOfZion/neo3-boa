from boa3.builtin.compile_time import public, CreateNewEvent
from boa3.builtin.contract import abort

Event = CreateNewEvent(
    [
        ('a', int)
    ],
    'example'
)


@public
def send_event():
    Event(10)


@public
def send_event_with_abort():
    send_event()
    abort()

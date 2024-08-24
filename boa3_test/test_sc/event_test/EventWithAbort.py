from boa3.sc.compiletime import public
from boa3.sc.utils import CreateNewEvent, abort

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

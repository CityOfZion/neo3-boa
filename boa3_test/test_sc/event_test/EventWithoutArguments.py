from boa3.sc.compiletime import public
from boa3.sc.utils import CreateNewEvent

Event = CreateNewEvent()


@public
def Main():
    Event()

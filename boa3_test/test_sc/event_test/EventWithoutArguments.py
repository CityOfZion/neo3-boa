from boa3.builtin.compile_time import public, CreateNewEvent

Event = CreateNewEvent()


@public
def Main():
    Event()

from boa3.builtin import CreateNewEvent, public

Event = CreateNewEvent()


@public
def Main():
    Event()

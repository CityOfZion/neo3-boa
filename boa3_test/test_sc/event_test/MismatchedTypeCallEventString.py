from boa3.builtin.compile_time import CreateNewEvent


Event = CreateNewEvent(
    [
        ('a', str)
    ]
)


def Main():
    Event(b'10')

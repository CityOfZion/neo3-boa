from boa3.builtin.compile_time import CreateNewEvent


Event = CreateNewEvent(
    [
        ('a', int)
    ]
)


def Main():
    Event('10')

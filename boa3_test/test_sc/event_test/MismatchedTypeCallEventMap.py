from boa3.builtin.compile_time import CreateNewEvent


Event = CreateNewEvent(
    [
        ('a', dict)
    ]
)


def Main():
    Event('10')

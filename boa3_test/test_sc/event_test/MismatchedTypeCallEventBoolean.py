from boa3.builtin.compile_time import CreateNewEvent


Event = CreateNewEvent(
    [
        ('a', bool)
    ]
)


def Main():
    Event('10')

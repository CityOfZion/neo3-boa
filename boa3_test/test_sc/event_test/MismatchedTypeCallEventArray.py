from boa3.builtin.compile_time import CreateNewEvent


Event = CreateNewEvent(
    [
        ('a', list)
    ]
)


def Main():
    Event('10')
